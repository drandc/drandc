"""
SQL Practice Generator - Main Flask Application
A comprehensive SQL practice application for mastering SQL skills
"""
import os
import sys
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (SECRET_KEY, DEBUG, SKILL_LEVELS, DATABASE_PATH,
                   EXERCISE_DB_PATH, DATA_SCENARIOS)
from database.db_manager import DatabaseManager, ExerciseDatabaseManager
from database.data_generator import DataGenerator
from exercises.generator import ExerciseGenerator, SessionManager
from exercises.exercise_loader import ExerciseLoader
from validation.validator import QueryValidator, ValidationEngine
from progress.tracker import ProgressTracker
from progress.achievements import AchievementManager, GamificationManager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Initialize components
def init_app():
    """Initialize application components"""
    # Initialize user database
    user_db = DatabaseManager(DATABASE_PATH)
    user_db.init_user_database()

    # Initialize exercise database if needed
    if not os.path.exists(EXERCISE_DB_PATH):
        print("Initializing exercise database...")
        generator = DataGenerator()
        generator.generate_all_scenarios()
        print("Exercise database initialized!")

init_app()

# Global instances
exercise_generator = ExerciseGenerator()
session_manager = SessionManager()
validator = ValidationEngine()
progress_tracker = ProgressTracker()
achievement_manager = AchievementManager()
gamification = GamificationManager()


# ============== Routes ==============

@app.route('/')
def index():
    """Dashboard / Home page"""
    stats = progress_tracker.get_overall_stats()
    suggestion = progress_tracker.get_suggested_next()
    motivation = gamification.get_motivation_message()
    daily_challenge = gamification.get_daily_challenge()

    return render_template('dashboard.html',
                          stats=stats,
                          suggestion=suggestion,
                          motivation=motivation,
                          daily_challenge=daily_challenge,
                          skill_levels=SKILL_LEVELS)


@app.route('/skills')
def skills():
    """Skill tree / topic selection page"""
    skills = progress_tracker.get_skill_status()
    return render_template('skills.html',
                          skills=skills,
                          skill_levels=SKILL_LEVELS)


@app.route('/exercise')
def exercise():
    """Exercise page"""
    # Get current exercise from session or generate new
    current = session_manager.get_current_exercise()
    if not current:
        # Redirect to skills page to start a session
        return redirect(url_for('skills'))

    # Get schema info for the exercise tables
    db = ExerciseDatabaseManager()
    schema = db.get_schema_info()

    # Filter to relevant tables
    if current.get('tables'):
        schema = {k: v for k, v in schema.items() if k in current['tables']}

    session_status = session_manager.get_session_status()

    return render_template('exercise.html',
                          exercise=current,
                          schema=schema,
                          session_status=session_status)


@app.route('/playground')
def playground():
    """SQL playground for free-form practice"""
    db = ExerciseDatabaseManager()
    schema = db.get_schema_info()
    return render_template('playground.html',
                          schema=schema,
                          scenarios=DATA_SCENARIOS)


@app.route('/stats')
def stats():
    """Statistics and progress page"""
    overall_stats = progress_tracker.get_overall_stats()
    achievements = achievement_manager.get_all_achievements()
    achievement_progress = achievement_manager.get_achievement_progress()
    weak_areas = progress_tracker.get_weak_areas()
    recent_history = progress_tracker.get_recent_history(20)

    return render_template('stats.html',
                          stats=overall_stats,
                          achievements=achievements,
                          achievement_progress=achievement_progress,
                          weak_areas=weak_areas,
                          history=recent_history)


@app.route('/settings')
def settings():
    """Settings page"""
    db = DatabaseManager(DATABASE_PATH)
    current_settings = {
        'validation_strictness': db.get_setting('validation_strictness', 'relaxed'),
        'case_sensitive': db.get_setting('case_sensitive', 'false'),
        'auto_advance': db.get_setting('auto_advance', 'false'),
        'show_execution_time': db.get_setting('show_execution_time', 'true'),
        'theme': db.get_setting('theme', 'light')
    }
    return render_template('settings.html', settings=current_settings)


# ============== API Routes ==============

@app.route('/api/start-session', methods=['POST'])
def api_start_session():
    """Start a new practice session"""
    data = request.json or {}

    levels = data.get('levels', [1])
    difficulties = data.get('difficulties', ['easy', 'medium', 'hard'])
    scenarios = data.get('scenarios')
    count = data.get('count', 10)

    # Convert levels to integers if they're strings
    levels = [int(l) for l in levels]

    session_info = session_manager.start_session(
        levels=levels,
        difficulties=difficulties,
        scenarios=scenarios,
        count=count
    )

    return jsonify({
        'success': True,
        'session': session_info
    })


@app.route('/api/current-exercise', methods=['GET'])
def api_current_exercise():
    """Get the current exercise"""
    exercise = session_manager.get_current_exercise()
    if not exercise:
        return jsonify({'success': False, 'error': 'No active session'})

    # Get schema for the exercise
    db = ExerciseDatabaseManager()
    schema = {}
    if exercise.get('tables'):
        for table in exercise['tables']:
            info = db.get_table_info(table)
            sample = db.get_sample_data(table, 5)
            count = db.get_row_count(table)
            schema[table] = {
                'columns': [dict(c) for c in info],
                'sample_data': sample,
                'row_count': count
            }

    return jsonify({
        'success': True,
        'exercise': exercise,
        'schema': schema,
        'session_status': session_manager.get_session_status()
    })


@app.route('/api/validate', methods=['POST'])
def api_validate():
    """Validate a user's query"""
    data = request.json
    user_query = data.get('query', '').strip()
    exercise_id = data.get('exercise_id')

    if not user_query:
        return jsonify({'success': False, 'error': 'Empty query'})

    # Get current exercise
    exercise = session_manager.get_current_exercise()
    if not exercise:
        return jsonify({'success': False, 'error': 'No active exercise'})

    # Track time
    start_time = time.time()

    # Validate the query
    result = validator.validate_exercise(user_query, exercise)

    # Calculate time taken
    time_taken = int(time.time() - start_time)

    # Record the attempt
    if result['is_correct']:
        progress_tracker.record_exercise(
            exercise_id=exercise.get('id', 'unknown'),
            level=exercise.get('level', 1),
            difficulty=exercise.get('difficulty', 'medium'),
            correct=True,
            time_taken=time_taken,
            user_query=user_query,
            hints_used=data.get('hints_used', 0),
            attempts=data.get('attempts', 1),
            scenario=exercise.get('scenario')
        )

        # Check for achievements
        gamification_result = gamification.process_exercise_complete(result)
        result['gamification'] = gamification_result

        # Mark as completed in session
        session_manager.mark_completed(True)

    return jsonify({
        'success': True,
        'result': result
    })


@app.route('/api/submit', methods=['POST'])
def api_submit():
    """Submit final answer (alias for validate with recording)"""
    return api_validate()


@app.route('/api/hint', methods=['POST'])
def api_hint():
    """Get a hint for the current exercise"""
    data = request.json
    hint_level = data.get('hint_level', 1)

    exercise = session_manager.get_current_exercise()
    if not exercise:
        return jsonify({'success': False, 'error': 'No active exercise'})

    hints = exercise.get('hints', [])
    available_hints = hints[:min(hint_level, len(hints))]

    return jsonify({
        'success': True,
        'hints': available_hints,
        'total_hints': len(hints),
        'current_level': min(hint_level, len(hints))
    })


@app.route('/api/solution', methods=['GET'])
def api_solution():
    """Get the solution for the current exercise"""
    exercise = session_manager.get_current_exercise()
    if not exercise:
        return jsonify({'success': False, 'error': 'No active exercise'})

    return jsonify({
        'success': True,
        'solution': exercise.get('solution', ''),
        'explanation': exercise.get('explanation', 'Study the solution to understand the approach.')
    })


@app.route('/api/next-exercise', methods=['POST'])
def api_next_exercise():
    """Move to the next exercise"""
    data = request.json or {}
    skip = data.get('skip', False)

    if skip:
        session_manager.skip_exercise()
    else:
        # If not skipping, we assume it was marked completed via validate
        pass

    exercise = session_manager.get_current_exercise()
    if not exercise:
        # Session complete
        summary = session_manager.end_session()
        return jsonify({
            'success': True,
            'session_complete': True,
            'summary': summary
        })

    return jsonify({
        'success': True,
        'session_complete': False,
        'session_status': session_manager.get_session_status()
    })


@app.route('/api/execute-playground', methods=['POST'])
def api_execute_playground():
    """Execute a query in playground mode"""
    data = request.json
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'success': False, 'error': 'Empty query'})

    query_validator = QueryValidator()
    result = query_validator.execute_playground_query(query)

    return jsonify(result)


@app.route('/api/schema/<table_name>', methods=['GET'])
def api_schema(table_name):
    """Get schema information for a specific table"""
    db = ExerciseDatabaseManager()
    info = db.get_table_info(table_name)
    sample = db.get_sample_data(table_name, 10)
    count = db.get_row_count(table_name)

    if not info:
        return jsonify({'success': False, 'error': 'Table not found'})

    return jsonify({
        'success': True,
        'table': table_name,
        'columns': [dict(c) for c in info],
        'sample_data': sample,
        'row_count': count
    })


@app.route('/api/skills', methods=['GET'])
def api_skills():
    """Get skill status"""
    skills = progress_tracker.get_skill_status()
    return jsonify({
        'success': True,
        'skills': skills
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get user statistics"""
    stats = progress_tracker.get_overall_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/achievements', methods=['GET'])
def api_achievements():
    """Get achievements"""
    achievements = achievement_manager.get_all_achievements()
    progress = achievement_manager.get_achievement_progress()
    return jsonify({
        'success': True,
        'achievements': achievements,
        'progress': progress
    })


@app.route('/api/settings', methods=['POST'])
def api_settings():
    """Update settings"""
    data = request.json
    db = DatabaseManager(DATABASE_PATH)

    for key, value in data.items():
        if key in ['validation_strictness', 'case_sensitive', 'auto_advance',
                   'show_execution_time', 'theme']:
            db.set_setting(key, str(value))

    return jsonify({'success': True})


@app.route('/api/export-progress', methods=['GET'])
def api_export_progress():
    """Export user progress"""
    data = progress_tracker.export_progress()
    return jsonify(data)


@app.route('/api/reset-progress', methods=['POST'])
def api_reset_progress():
    """Reset user progress (requires confirmation)"""
    data = request.json
    if data.get('confirm') != 'RESET':
        return jsonify({'success': False, 'error': 'Confirmation required'})

    progress_tracker.reset_progress()
    return jsonify({'success': True, 'message': 'Progress reset successfully'})


@app.route('/api/generate-exercise', methods=['POST'])
def api_generate_exercise():
    """Generate a single exercise without starting a session"""
    data = request.json or {}

    level = data.get('level', 1)
    difficulty = data.get('difficulty')
    scenario = data.get('scenario')

    exercise = exercise_generator.generate_exercise(
        level=level,
        difficulty=difficulty,
        scenario=scenario
    )

    if not exercise:
        return jsonify({'success': False, 'error': 'No matching exercise found'})

    return jsonify({
        'success': True,
        'exercise': exercise
    })


# ============== Error Handlers ==============

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error='Server error'), 500


# ============== Main Entry Point ==============

if __name__ == '__main__':
    print("=" * 60)
    print("SQL Practice Generator")
    print("=" * 60)
    print(f"Starting server at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5000, debug=DEBUG)
