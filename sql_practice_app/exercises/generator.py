"""
Exercise Generator for SQL Practice Generator
Generates exercise instances from templates
"""
import random
import copy
from typing import List, Dict, Any, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SKILL_LEVELS, DATA_SCENARIOS
from exercises.exercise_loader import ExerciseLoader


class ExerciseGenerator:
    """Generates exercises from templates with dynamic substitution"""

    def __init__(self):
        self.loader = ExerciseLoader()
        self.used_exercises = set()  # Track used exercises to avoid repetition

    def generate_exercise(self, level: int = None, difficulty: str = None,
                          scenario: str = None, exclude_ids: List[str] = None) -> Optional[Dict]:
        """
        Generate a single exercise matching the criteria

        Args:
            level: Skill level (1-13)
            difficulty: 'easy', 'medium', or 'hard'
            scenario: Data scenario name
            exclude_ids: List of exercise IDs to exclude

        Returns:
            Exercise dictionary or None if no matching template found
        """
        # Get matching templates
        templates = self.loader.get_templates_filtered(
            levels=[level] if level else None,
            difficulties=[difficulty] if difficulty else None,
            scenarios=[scenario] if scenario else None
        )

        # Exclude used exercises
        if exclude_ids:
            templates = [t for t in templates if t['id'] not in exclude_ids]

        # Also exclude recently used
        templates = [t for t in templates if t['id'] not in self.used_exercises]

        if not templates:
            # If all templates used, reset and try again
            self.used_exercises.clear()
            templates = self.loader.get_templates_filtered(
                levels=[level] if level else None,
                difficulties=[difficulty] if difficulty else None,
                scenarios=[scenario] if scenario else None
            )
            if exclude_ids:
                templates = [t for t in templates if t['id'] not in exclude_ids]

        if not templates:
            return None

        # Select a random template
        template = random.choice(templates)
        self.used_exercises.add(template['id'])

        # Create exercise instance from template
        exercise = self._create_exercise_instance(template)

        return exercise

    def _create_exercise_instance(self, template: Dict) -> Dict:
        """Create an exercise instance from a template"""
        exercise = copy.deepcopy(template)

        # Apply any variable substitutions
        if 'variables' in template:
            for var_name, var_values in template['variables'].items():
                selected_value = random.choice(var_values)
                exercise['problem'] = exercise['problem'].replace(
                    f'{{{var_name}}}', str(selected_value)
                )
                if 'solution' in exercise:
                    exercise['solution'] = exercise['solution'].replace(
                        f'{{{var_name}}}', str(selected_value)
                    )

        # Add metadata
        exercise['instance_id'] = f"{template['id']}_{random.randint(1000, 9999)}"
        exercise['level_name'] = SKILL_LEVELS.get(template['level'], {}).get('name', 'Unknown')

        return exercise

    def generate_session(self, levels: List[int] = None,
                         difficulties: List[str] = None,
                         scenarios: List[str] = None,
                         count: int = 10) -> List[Dict]:
        """
        Generate a practice session with multiple exercises

        Args:
            levels: List of levels to include
            difficulties: List of difficulties to include
            scenarios: List of scenarios to include
            count: Number of exercises to generate

        Returns:
            List of exercise dictionaries
        """
        exercises = []
        exclude_ids = []

        for _ in range(count):
            # Randomly select from the allowed options
            level = random.choice(levels) if levels else None
            difficulty = random.choice(difficulties) if difficulties else None
            scenario = random.choice(scenarios) if scenarios else None

            exercise = self.generate_exercise(
                level=level,
                difficulty=difficulty,
                scenario=scenario,
                exclude_ids=exclude_ids
            )

            if exercise:
                exercises.append(exercise)
                exclude_ids.append(exercise['id'])

        return exercises

    def generate_progressive_session(self, start_level: int, count: int = 10,
                                     difficulty_progression: bool = True) -> List[Dict]:
        """
        Generate a session with progressive difficulty

        Args:
            start_level: Starting skill level
            count: Number of exercises
            difficulty_progression: If True, start with easy and progress

        Returns:
            List of exercise dictionaries
        """
        exercises = []
        exclude_ids = []

        if difficulty_progression:
            difficulties = ['easy'] * (count // 3) + ['medium'] * (count // 3) + ['hard'] * (count - 2 * (count // 3))
        else:
            difficulties = ['easy', 'medium', 'hard'] * (count // 3 + 1)
            difficulties = difficulties[:count]

        for i, difficulty in enumerate(difficulties):
            # Gradually increase level
            level = min(start_level + (i // 3), 13)

            exercise = self.generate_exercise(
                level=level,
                difficulty=difficulty,
                exclude_ids=exclude_ids
            )

            if exercise:
                exercises.append(exercise)
                exclude_ids.append(exercise['id'])

        return exercises

    def generate_topic_practice(self, level: int, count: int = 5) -> List[Dict]:
        """
        Generate exercises focused on a specific level/topic

        Args:
            level: The skill level to practice
            count: Number of exercises

        Returns:
            List of exercise dictionaries
        """
        exercises = []
        exclude_ids = []

        # Get exercises at this level
        for _ in range(count):
            exercise = self.generate_exercise(
                level=level,
                exclude_ids=exclude_ids
            )

            if exercise:
                exercises.append(exercise)
                exclude_ids.append(exercise['id'])

        return exercises

    def generate_mixed_review(self, mastered_levels: List[int], count: int = 10) -> List[Dict]:
        """
        Generate a review session covering multiple mastered levels

        Args:
            mastered_levels: List of levels the user has completed
            count: Number of exercises

        Returns:
            List of exercise dictionaries
        """
        exercises = []
        exclude_ids = []

        for _ in range(count):
            level = random.choice(mastered_levels)
            difficulty = random.choices(['easy', 'medium', 'hard'],
                                       weights=[20, 50, 30])[0]

            exercise = self.generate_exercise(
                level=level,
                difficulty=difficulty,
                exclude_ids=exclude_ids
            )

            if exercise:
                exercises.append(exercise)
                exclude_ids.append(exercise['id'])

        return exercises

    def get_exercise_by_id(self, exercise_id: str) -> Optional[Dict]:
        """Get a specific exercise by template ID"""
        template = self.loader.get_template(exercise_id)
        if template:
            return self._create_exercise_instance(template)
        return None

    def get_available_exercises_count(self, level: int = None,
                                      difficulty: str = None,
                                      scenario: str = None) -> int:
        """Get count of available exercises matching criteria"""
        templates = self.loader.get_templates_filtered(
            levels=[level] if level else None,
            difficulties=[difficulty] if difficulty else None,
            scenarios=[scenario] if scenario else None
        )
        return len(templates)

    def get_statistics(self) -> Dict[str, Any]:
        """Get exercise generation statistics"""
        return {
            'template_stats': self.loader.get_statistics(),
            'used_count': len(self.used_exercises),
            'available_levels': list(range(1, 14)),
            'available_difficulties': ['easy', 'medium', 'hard'],
            'available_scenarios': DATA_SCENARIOS
        }

    def reset_used_exercises(self):
        """Reset the used exercises tracking"""
        self.used_exercises.clear()


class SessionManager:
    """Manages practice sessions"""

    def __init__(self):
        self.generator = ExerciseGenerator()
        self.current_session = None
        self.current_index = 0

    def start_session(self, levels: List[int] = None,
                      difficulties: List[str] = None,
                      scenarios: List[str] = None,
                      count: int = 10) -> Dict:
        """
        Start a new practice session

        Returns:
            Session info dictionary
        """
        self.generator.reset_used_exercises()

        # Generate exercises for the session
        exercises = self.generator.generate_session(
            levels=levels,
            difficulties=difficulties,
            scenarios=scenarios,
            count=count
        )

        self.current_session = {
            'exercises': exercises,
            'total': len(exercises),
            'completed': 0,
            'correct': 0,
            'levels': levels or list(range(1, 14)),
            'difficulties': difficulties or ['easy', 'medium', 'hard'],
            'scenarios': scenarios or DATA_SCENARIOS
        }
        self.current_index = 0

        return {
            'session_id': id(self.current_session),
            'total_exercises': len(exercises),
            'levels': levels,
            'difficulties': difficulties,
            'scenarios': scenarios
        }

    def get_current_exercise(self) -> Optional[Dict]:
        """Get the current exercise in the session"""
        if not self.current_session or self.current_index >= len(self.current_session['exercises']):
            return None
        return self.current_session['exercises'][self.current_index]

    def mark_completed(self, correct: bool) -> Dict:
        """
        Mark current exercise as completed

        Returns:
            Progress info dictionary
        """
        if not self.current_session:
            return {'error': 'No active session'}

        self.current_session['completed'] += 1
        if correct:
            self.current_session['correct'] += 1

        self.current_index += 1

        return {
            'completed': self.current_session['completed'],
            'correct': self.current_session['correct'],
            'remaining': self.current_session['total'] - self.current_session['completed'],
            'accuracy': round(self.current_session['correct'] / self.current_session['completed'] * 100, 1)
        }

    def get_session_status(self) -> Optional[Dict]:
        """Get current session status"""
        if not self.current_session:
            return None

        return {
            'total': self.current_session['total'],
            'completed': self.current_session['completed'],
            'correct': self.current_session['correct'],
            'remaining': self.current_session['total'] - self.current_session['completed'],
            'accuracy': round(self.current_session['correct'] / max(self.current_session['completed'], 1) * 100, 1),
            'current_index': self.current_index
        }

    def end_session(self) -> Dict:
        """End the current session and return summary"""
        if not self.current_session:
            return {'error': 'No active session'}

        summary = {
            'total': self.current_session['total'],
            'completed': self.current_session['completed'],
            'correct': self.current_session['correct'],
            'accuracy': round(self.current_session['correct'] / max(self.current_session['completed'], 1) * 100, 1)
        }

        self.current_session = None
        self.current_index = 0

        return summary

    def skip_exercise(self) -> Optional[Dict]:
        """Skip the current exercise and move to next"""
        if not self.current_session:
            return None

        self.current_index += 1
        return self.get_current_exercise()
