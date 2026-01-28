"""
Progress Tracker for SQL Practice Generator
Tracks user progress, skill mastery, and unlocks
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (SKILL_LEVELS, MASTERY_LEVELS, UNLOCK_THRESHOLD,
                   UNLOCK_SUCCESS_RATE, DATABASE_PATH)
from database.db_manager import DatabaseManager


class ProgressTracker:
    """Tracks user progress and manages skill unlocking"""

    def __init__(self, db_path: str = DATABASE_PATH):
        """
        Initialize the progress tracker

        Args:
            db_path: Path to the user database
        """
        self.db = DatabaseManager(db_path)
        self.db.init_user_database()

    def record_exercise(self, exercise_id: str, level: int, difficulty: str,
                       correct: bool, time_taken: int, user_query: str,
                       hints_used: int = 0, attempts: int = 1,
                       scenario: str = None) -> Dict[str, Any]:
        """
        Record an exercise attempt

        Args:
            exercise_id: ID of the exercise
            level: Skill level
            difficulty: Difficulty level
            correct: Whether the answer was correct
            time_taken: Time taken in seconds
            user_query: The user's query
            hints_used: Number of hints used
            attempts: Number of attempts
            scenario: Data scenario used

        Returns:
            Updated progress info
        """
        # Record to exercise history
        self.db.add_exercise_history(
            exercise_id=exercise_id,
            level=level,
            difficulty=difficulty,
            correct=correct,
            time_taken=time_taken,
            user_query=user_query,
            hints_used=hints_used,
            attempts=attempts,
            scenario=scenario
        )

        # Update user stats
        self._update_user_stats(correct)

        # Update skill progress
        skill_name = SKILL_LEVELS.get(level, {}).get('name', 'Unknown')
        self._update_skill_progress(skill_name, level, correct)

        # Check for new unlocks
        new_unlocks = self._check_unlocks()

        # Check for achievements (handled by AchievementManager)

        return {
            'exercise_recorded': True,
            'new_unlocks': new_unlocks,
            'current_streak': self.get_current_streak()
        }

    def _update_user_stats(self, correct: bool):
        """Update user statistics after an exercise"""
        stats = self.db.get_user_stats()

        new_total = stats.get('total_exercises', 0) + 1
        new_correct = stats.get('total_correct', 0) + (1 if correct else 0)

        # Update streak
        current_streak = stats.get('current_streak', 0)
        longest_streak = stats.get('longest_streak', 0)

        if correct:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0

        # Update day streak
        today = datetime.now().strftime('%Y-%m-%d')
        last_practice = stats.get('last_practice_date')

        day_streak = stats.get('day_streak', 0)
        if last_practice:
            last_date = datetime.strptime(last_practice, '%Y-%m-%d')
            today_date = datetime.strptime(today, '%Y-%m-%d')
            days_diff = (today_date - last_date).days

            if days_diff == 0:
                pass  # Same day, no change
            elif days_diff == 1:
                day_streak += 1  # Consecutive day
            else:
                day_streak = 1  # Streak broken
        else:
            day_streak = 1

        self.db.update_user_stats(
            total_exercises=new_total,
            total_correct=new_correct,
            current_streak=current_streak,
            longest_streak=longest_streak,
            day_streak=day_streak,
            last_practice_date=today
        )

    def _update_skill_progress(self, skill_name: str, level: int, correct: bool):
        """Update progress for a specific skill"""
        skills = self.db.get_skill_progress(level)
        if not skills:
            return

        skill = skills[0]
        new_completed = skill.get('exercises_completed', 0) + 1
        new_correct = skill.get('exercises_correct', 0) + (1 if correct else 0)

        # Calculate new mastery level
        mastery = self._calculate_mastery(new_completed, new_correct)

        self.db.update_skill_progress(
            skill_name,
            exercises_completed=new_completed,
            exercises_correct=new_correct,
            mastery_level=mastery,
            last_practiced=datetime.now().isoformat()
        )

    def _calculate_mastery(self, completed: int, correct: int) -> str:
        """Calculate mastery level based on exercises completed"""
        if completed >= MASTERY_LEVELS['platinum']:
            return 'platinum'
        elif completed >= MASTERY_LEVELS['gold']:
            return 'gold'
        elif completed >= MASTERY_LEVELS['silver']:
            return 'silver'
        elif completed >= MASTERY_LEVELS['bronze']:
            return 'bronze'
        return 'none'

    def _check_unlocks(self) -> List[Dict[str, Any]]:
        """Check if any new skills should be unlocked"""
        unlocks = []
        skills = self.db.get_skill_progress()

        for skill in skills:
            if skill['unlocked']:
                continue

            level = skill['level']
            if level == 1:
                # Level 1 is always unlocked
                self.db.update_skill_progress(skill['skill_name'], unlocked=True)
                continue

            # Check if prerequisites are met
            prereq_level = level - 1
            prereq_skills = [s for s in skills if s['level'] == prereq_level]

            if prereq_skills:
                prereq = prereq_skills[0]
                completed = prereq.get('exercises_completed', 0)
                correct = prereq.get('exercises_correct', 0)

                if completed >= UNLOCK_THRESHOLD:
                    success_rate = correct / completed if completed > 0 else 0
                    if success_rate >= UNLOCK_SUCCESS_RATE:
                        self.db.update_skill_progress(skill['skill_name'], unlocked=True)
                        unlocks.append({
                            'skill_name': skill['skill_name'],
                            'level': level
                        })

        return unlocks

    def get_current_streak(self) -> int:
        """Get current correct answer streak"""
        stats = self.db.get_user_stats()
        return stats.get('current_streak', 0)

    def get_day_streak(self) -> int:
        """Get current day streak"""
        stats = self.db.get_user_stats()
        return stats.get('day_streak', 0)

    def get_skill_status(self, level: int = None) -> List[Dict[str, Any]]:
        """
        Get status of skills

        Args:
            level: Specific level to get, or None for all

        Returns:
            List of skill status dictionaries
        """
        skills = self.db.get_skill_progress(level)
        result = []

        for skill in skills:
            skill_info = SKILL_LEVELS.get(skill['level'], {})
            result.append({
                'name': skill['skill_name'],
                'level': skill['level'],
                'description': skill_info.get('description', ''),
                'skills': skill_info.get('skills', []),
                'exercises_completed': skill['exercises_completed'],
                'exercises_correct': skill['exercises_correct'],
                'mastery_level': skill['mastery_level'],
                'unlocked': skill['unlocked'],
                'last_practiced': skill['last_practiced'],
                'success_rate': round(
                    (skill['exercises_correct'] / max(skill['exercises_completed'], 1)) * 100, 1
                ),
                'progress_to_next': self._get_progress_to_next_mastery(skill)
            })

        return result

    def _get_progress_to_next_mastery(self, skill: Dict) -> Dict[str, Any]:
        """Calculate progress to next mastery level"""
        completed = skill.get('exercises_completed', 0)
        current_mastery = skill.get('mastery_level', 'none')

        # Find next level threshold
        levels = ['none', 'bronze', 'silver', 'gold', 'platinum']
        current_idx = levels.index(current_mastery)

        if current_idx >= len(levels) - 1:
            return {'at_max': True}

        next_level = levels[current_idx + 1]
        next_threshold = MASTERY_LEVELS[next_level]

        return {
            'next_level': next_level,
            'current': completed,
            'required': next_threshold,
            'remaining': max(0, next_threshold - completed),
            'percentage': min(100, round((completed / next_threshold) * 100, 1))
        }

    def get_overall_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        stats = self.db.get_user_stats()
        skills = self.get_skill_status()

        total_exercises = stats.get('total_exercises', 0)
        total_correct = stats.get('total_correct', 0)

        return {
            'total_exercises': total_exercises,
            'total_correct': total_correct,
            'accuracy': round((total_correct / max(total_exercises, 1)) * 100, 1),
            'current_streak': stats.get('current_streak', 0),
            'longest_streak': stats.get('longest_streak', 0),
            'day_streak': stats.get('day_streak', 0),
            'last_practice': stats.get('last_practice_date'),
            'unlocked_levels': sum(1 for s in skills if s['unlocked']),
            'total_levels': len(skills),
            'skills': skills
        }

    def get_recent_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent exercise history"""
        return self.db.get_exercise_history(limit)

    def get_weak_areas(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Identify areas that need more practice"""
        skills = self.get_skill_status()
        weak = []

        for skill in skills:
            if not skill['unlocked']:
                continue
            if skill['exercises_completed'] < 5:
                continue

            # Low success rate
            if skill['success_rate'] < 70:
                weak.append({
                    'skill': skill['name'],
                    'level': skill['level'],
                    'reason': 'low_accuracy',
                    'success_rate': skill['success_rate'],
                    'recommendation': f"Practice more {skill['name']} exercises to improve accuracy"
                })

            # Haven't practiced recently
            if skill['last_practiced']:
                last = datetime.fromisoformat(skill['last_practiced'])
                if datetime.now() - last > timedelta(days=7):
                    weak.append({
                        'skill': skill['name'],
                        'level': skill['level'],
                        'reason': 'not_recent',
                        'last_practiced': skill['last_practiced'],
                        'recommendation': f"It's been a while since you practiced {skill['name']}"
                    })

        # Sort by success rate
        weak.sort(key=lambda x: x.get('success_rate', 100))
        return weak[:limit]

    def get_suggested_next(self) -> Dict[str, Any]:
        """Suggest what to practice next"""
        skills = self.get_skill_status()

        # Priority 1: New unlocked skills with few exercises
        for skill in skills:
            if skill['unlocked'] and skill['exercises_completed'] < 5:
                return {
                    'type': 'new_skill',
                    'skill': skill['name'],
                    'level': skill['level'],
                    'reason': 'You have a new skill to explore!'
                }

        # Priority 2: Skills close to next mastery
        for skill in skills:
            if skill['unlocked']:
                progress = skill['progress_to_next']
                if not progress.get('at_max') and progress.get('percentage', 0) > 80:
                    return {
                        'type': 'close_to_mastery',
                        'skill': skill['name'],
                        'level': skill['level'],
                        'reason': f"You're close to reaching {progress['next_level']} mastery!"
                    }

        # Priority 3: Weak areas
        weak = self.get_weak_areas(1)
        if weak:
            return {
                'type': 'weak_area',
                'skill': weak[0]['skill'],
                'level': weak[0]['level'],
                'reason': weak[0]['recommendation']
            }

        # Priority 4: Random unlocked skill
        unlocked = [s for s in skills if s['unlocked']]
        if unlocked:
            import random
            skill = random.choice(unlocked)
            return {
                'type': 'continue_practice',
                'skill': skill['name'],
                'level': skill['level'],
                'reason': 'Keep practicing to maintain your skills!'
            }

        return {
            'type': 'start',
            'skill': 'Foundation',
            'level': 1,
            'reason': 'Start with the basics!'
        }

    def export_progress(self) -> Dict[str, Any]:
        """Export all progress data for backup"""
        return {
            'exported_at': datetime.now().isoformat(),
            'stats': self.db.get_user_stats(),
            'skills': self.db.get_skill_progress(),
            'achievements': self.db.get_achievements(),
            'history': self.db.get_exercise_history(limit=1000)
        }

    def reset_progress(self):
        """Reset all progress (careful!)"""
        self.db.execute_script("""
            UPDATE user_stats SET
                total_exercises = 0,
                total_correct = 0,
                current_streak = 0,
                longest_streak = 0,
                day_streak = 0,
                last_practice_date = NULL
            WHERE user_id = 1;

            UPDATE skill_progress SET
                exercises_completed = 0,
                exercises_correct = 0,
                mastery_level = 'none',
                unlocked = CASE WHEN level = 1 THEN 1 ELSE 0 END,
                last_practiced = NULL;

            DELETE FROM exercise_history;
            DELETE FROM achievements;
        """)
