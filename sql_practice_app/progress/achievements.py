"""
Achievement Manager for SQL Practice Generator
Manages unlocking and tracking achievements
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ACHIEVEMENTS, DATABASE_PATH
from database.db_manager import DatabaseManager


class AchievementManager:
    """Manages achievements and badges"""

    def __init__(self, db_path: str = DATABASE_PATH):
        """
        Initialize the achievement manager

        Args:
            db_path: Path to the user database
        """
        self.db = DatabaseManager(db_path)
        self.achievements = ACHIEVEMENTS

    def check_achievements(self, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Check for newly unlocked achievements

        Args:
            context: Additional context for checking (current exercise info, etc.)

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []
        stats = self.db.get_user_stats()
        current_achievements = {a['achievement_id']: a for a in self.db.get_achievements()}

        for ach_id, ach_info in self.achievements.items():
            # Skip if already unlocked
            if ach_id in current_achievements and current_achievements[ach_id].get('unlocked'):
                continue

            # Check if condition is met
            if self._check_condition(ach_id, stats, context):
                self.db.unlock_achievement(
                    ach_id,
                    ach_info['name'],
                    ach_info['description']
                )
                newly_unlocked.append({
                    'id': ach_id,
                    'name': ach_info['name'],
                    'description': ach_info['description'],
                    'icon': ach_info.get('icon', 'trophy')
                })

        return newly_unlocked

    def _check_condition(self, ach_id: str, stats: Dict, context: Dict = None) -> bool:
        """Check if an achievement condition is met"""
        context = context or {}

        total_exercises = stats.get('total_exercises', 0)
        current_streak = stats.get('current_streak', 0)
        day_streak = stats.get('day_streak', 0)

        # First Steps - Complete first exercise
        if ach_id == 'first_steps':
            return total_exercises >= 1

        # Perfectionist - 10 in a row
        if ach_id == 'perfectionist':
            return current_streak >= 10

        # Speed Demon - Under 60 seconds
        if ach_id == 'speed_demon':
            if context.get('time_taken'):
                return context['time_taken'] < 60 and context.get('correct', False)
            return False

        # Persistent - Solve after 3+ attempts
        if ach_id == 'persistent':
            if context.get('attempts'):
                return context['attempts'] >= 3 and context.get('correct', False)
            return False

        # Diverse Learner - All levels in one week
        if ach_id == 'diverse_learner':
            return self._check_weekly_diversity()

        # SQL Master - 500 exercises
        if ach_id == 'sql_master':
            return total_exercises >= 500

        # Century - 100 exercises
        if ach_id == 'century':
            return total_exercises >= 100

        # Week Warrior - 7 day streak
        if ach_id == 'week_warrior':
            return day_streak >= 7

        # Join Master - 20 join exercises
        if ach_id == 'join_master':
            return self._count_level_exercises([4, 5]) >= 20

        # Aggregation Pro - 20 aggregation exercises
        if ach_id == 'aggregation_pro':
            return self._count_level_exercises([3]) >= 20

        return False

    def _check_weekly_diversity(self) -> bool:
        """Check if user practiced all levels in the past week"""
        one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        history = self.db.execute("""
            SELECT DISTINCT level FROM exercise_history
            WHERE attempted_at >= ? AND correct = 1
        """, (one_week_ago,))

        levels_practiced = {row['level'] for row in history}
        return len(levels_practiced) >= 13

    def _count_level_exercises(self, levels: List[int]) -> int:
        """Count exercises completed for specific levels"""
        placeholders = ','.join('?' * len(levels))
        result = self.db.execute(f"""
            SELECT COUNT(*) as count FROM exercise_history
            WHERE level IN ({placeholders}) AND correct = 1
        """, tuple(levels))
        return result[0]['count'] if result else 0

    def get_all_achievements(self) -> List[Dict[str, Any]]:
        """Get all achievements with their status"""
        unlocked = {a['achievement_id']: a for a in self.db.get_achievements()}

        result = []
        for ach_id, ach_info in self.achievements.items():
            is_unlocked = ach_id in unlocked and unlocked[ach_id].get('unlocked')
            result.append({
                'id': ach_id,
                'name': ach_info['name'],
                'description': ach_info['description'],
                'icon': ach_info.get('icon', 'trophy'),
                'unlocked': is_unlocked,
                'unlocked_at': unlocked.get(ach_id, {}).get('unlocked_at') if is_unlocked else None
            })

        # Sort: unlocked first, then by name
        result.sort(key=lambda x: (not x['unlocked'], x['name']))
        return result

    def get_unlocked_achievements(self) -> List[Dict[str, Any]]:
        """Get only unlocked achievements"""
        return [a for a in self.get_all_achievements() if a['unlocked']]

    def get_locked_achievements(self) -> List[Dict[str, Any]]:
        """Get only locked achievements"""
        return [a for a in self.get_all_achievements() if not a['unlocked']]

    def get_achievement_progress(self) -> Dict[str, Any]:
        """Get overall achievement progress"""
        all_achievements = self.get_all_achievements()
        unlocked = [a for a in all_achievements if a['unlocked']]

        return {
            'total': len(all_achievements),
            'unlocked': len(unlocked),
            'locked': len(all_achievements) - len(unlocked),
            'percentage': round((len(unlocked) / len(all_achievements)) * 100, 1),
            'recent': unlocked[-3:] if unlocked else []
        }

    def get_next_achievable(self, stats: Dict = None) -> List[Dict[str, Any]]:
        """Get achievements that are close to being unlocked"""
        if stats is None:
            stats = self.db.get_user_stats()

        locked = self.get_locked_achievements()
        close_achievements = []

        for ach in locked:
            progress = self._get_achievement_progress(ach['id'], stats)
            if progress and progress.get('percentage', 0) > 0:
                close_achievements.append({
                    **ach,
                    'progress': progress
                })

        # Sort by progress percentage
        close_achievements.sort(key=lambda x: x['progress'].get('percentage', 0), reverse=True)
        return close_achievements[:5]

    def _get_achievement_progress(self, ach_id: str, stats: Dict) -> Optional[Dict[str, Any]]:
        """Get progress towards a specific achievement"""
        total_exercises = stats.get('total_exercises', 0)
        current_streak = stats.get('current_streak', 0)
        day_streak = stats.get('day_streak', 0)

        progress_map = {
            'first_steps': {
                'current': min(total_exercises, 1),
                'required': 1,
                'percentage': min(100, total_exercises * 100)
            },
            'perfectionist': {
                'current': current_streak,
                'required': 10,
                'percentage': min(100, (current_streak / 10) * 100)
            },
            'sql_master': {
                'current': total_exercises,
                'required': 500,
                'percentage': min(100, (total_exercises / 500) * 100)
            },
            'century': {
                'current': total_exercises,
                'required': 100,
                'percentage': min(100, (total_exercises / 100) * 100)
            },
            'week_warrior': {
                'current': day_streak,
                'required': 7,
                'percentage': min(100, (day_streak / 7) * 100)
            },
            'join_master': {
                'current': self._count_level_exercises([4, 5]),
                'required': 20,
                'percentage': min(100, (self._count_level_exercises([4, 5]) / 20) * 100)
            },
            'aggregation_pro': {
                'current': self._count_level_exercises([3]),
                'required': 20,
                'percentage': min(100, (self._count_level_exercises([3]) / 20) * 100)
            }
        }

        progress = progress_map.get(ach_id)
        if progress:
            progress['percentage'] = round(progress['percentage'], 1)
        return progress


class GamificationManager:
    """High-level gamification management"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db = DatabaseManager(db_path)
        self.achievements = AchievementManager(db_path)

    def process_exercise_complete(self, exercise_result: Dict) -> Dict[str, Any]:
        """
        Process gamification after exercise completion

        Args:
            exercise_result: Result from exercise validation

        Returns:
            Gamification updates (achievements, streak, etc.)
        """
        context = {
            'correct': exercise_result.get('is_correct', False),
            'time_taken': exercise_result.get('execution_time', 0),
            'attempts': exercise_result.get('attempts', 1),
            'level': exercise_result.get('level', 1)
        }

        # Check for new achievements
        new_achievements = self.achievements.check_achievements(context)

        # Get current stats
        stats = self.db.get_user_stats()

        return {
            'new_achievements': new_achievements,
            'current_streak': stats.get('current_streak', 0),
            'day_streak': stats.get('day_streak', 0),
            'total_exercises': stats.get('total_exercises', 0)
        }

    def get_motivation_message(self) -> str:
        """Get a motivational message based on current progress"""
        stats = self.db.get_user_stats()

        messages = [
            "Keep up the great work!",
            "Every query makes you stronger!",
            "SQL mastery is within reach!",
            "You're making excellent progress!",
            "Practice makes perfect!"
        ]

        streak = stats.get('current_streak', 0)
        if streak >= 10:
            return f"Amazing! {streak} correct in a row!"
        elif streak >= 5:
            return f"Great streak! {streak} correct answers!"
        elif streak >= 3:
            return f"Nice! {streak} in a row - keep going!"

        total = stats.get('total_exercises', 0)
        if total >= 100:
            return "Over 100 exercises completed - you're dedicated!"
        elif total >= 50:
            return "Halfway to 100 exercises!"
        elif total >= 10:
            return "Great start! Keep the momentum going!"

        import random
        return random.choice(messages)

    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get a daily challenge for the user"""
        import random

        challenges = [
            {
                'type': 'exercises',
                'target': 5,
                'description': 'Complete 5 exercises today',
                'reward': '50 XP'
            },
            {
                'type': 'accuracy',
                'target': 80,
                'description': 'Achieve 80% accuracy today',
                'reward': 'Speed Boost'
            },
            {
                'type': 'streak',
                'target': 3,
                'description': 'Get 3 correct in a row',
                'reward': 'Streak Shield'
            },
            {
                'type': 'level',
                'target': 'any',
                'description': 'Try a new skill level',
                'reward': 'Explorer Badge'
            },
            {
                'type': 'time',
                'target': 120,
                'description': 'Complete an exercise in under 2 minutes',
                'reward': 'Time Master'
            }
        ]

        # Use date as seed for consistent daily challenge
        today = datetime.now().strftime('%Y-%m-%d')
        random.seed(hash(today))
        challenge = random.choice(challenges)
        random.seed()  # Reset seed

        return {
            'challenge': challenge,
            'date': today,
            'completed': False  # Would check against history
        }
