"""
Database Manager for SQL Practice Generator
Handles all database connections and setup
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_PATH, EXERCISE_DB_PATH


class DatabaseManager:
    """Manages SQLite database connections and operations"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a query and return results as list of dicts"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            columns = [description[0] for description in cursor.description] if cursor.description else []
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute a query with multiple parameter sets"""
        with self.get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            return cursor.rowcount

    def execute_script(self, script: str):
        """Execute a multi-statement SQL script"""
        with self.get_connection() as conn:
            conn.executescript(script)

    def init_user_database(self):
        """Initialize the user progress database"""
        schema = """
        -- User statistics table
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY DEFAULT 1,
            total_exercises INTEGER DEFAULT 0,
            total_correct INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            day_streak INTEGER DEFAULT 0,
            last_practice_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Exercise history table
        CREATE TABLE IF NOT EXISTS exercise_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id TEXT NOT NULL,
            level INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            scenario TEXT,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            correct BOOLEAN NOT NULL,
            time_taken_seconds INTEGER,
            user_query TEXT,
            hints_used INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 1
        );

        -- Skill progress table
        CREATE TABLE IF NOT EXISTS skill_progress (
            skill_name TEXT PRIMARY KEY,
            level INTEGER NOT NULL,
            exercises_completed INTEGER DEFAULT 0,
            exercises_correct INTEGER DEFAULT 0,
            mastery_level TEXT DEFAULT 'none',
            unlocked BOOLEAN DEFAULT 0,
            last_practiced TIMESTAMP
        );

        -- Achievements table
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            unlocked BOOLEAN DEFAULT 0,
            unlocked_at TIMESTAMP
        );

        -- Session history table
        CREATE TABLE IF NOT EXISTS session_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            exercises_attempted INTEGER DEFAULT 0,
            exercises_correct INTEGER DEFAULT 0,
            levels_practiced TEXT,
            difficulties TEXT
        );

        -- Saved queries table
        CREATE TABLE IF NOT EXISTS saved_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            query TEXT NOT NULL,
            scenario TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Settings table
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        -- Initialize default user stats if not exists
        INSERT OR IGNORE INTO user_stats (user_id) VALUES (1);

        -- Initialize skill progress for all levels
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Foundation', 1, 1);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Sorting & Uniqueness', 2, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Aggregation Basics', 3, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Basic Joins', 4, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Advanced Joins', 5, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Subqueries', 6, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Conditional Logic', 7, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Window Functions', 8, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('CTEs', 9, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Advanced CTEs', 10, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Optimization', 11, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Data Manipulation', 12, 0);
        INSERT OR IGNORE INTO skill_progress (skill_name, level, unlocked) VALUES ('Advanced Topics', 13, 0);

        -- Initialize default settings
        INSERT OR IGNORE INTO settings (key, value) VALUES ('validation_strictness', 'relaxed');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('case_sensitive', 'false');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('auto_advance', 'false');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('show_execution_time', 'true');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'light');
        """
        self.execute_script(schema)

    def get_user_stats(self) -> Dict[str, Any]:
        """Get current user statistics"""
        result = self.execute("SELECT * FROM user_stats WHERE user_id = 1")
        return result[0] if result else {}

    def update_user_stats(self, **kwargs):
        """Update user statistics"""
        valid_fields = ['total_exercises', 'total_correct', 'current_streak',
                       'longest_streak', 'day_streak', 'last_practice_date']
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        if not updates:
            return

        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE user_stats SET {set_clause} WHERE user_id = 1"
        with self.get_connection() as conn:
            conn.execute(query, tuple(updates.values()))

    def get_skill_progress(self, level: Optional[int] = None) -> List[Dict]:
        """Get skill progress, optionally filtered by level"""
        if level:
            return self.execute(
                "SELECT * FROM skill_progress WHERE level = ?", (level,)
            )
        return self.execute("SELECT * FROM skill_progress ORDER BY level")

    def update_skill_progress(self, skill_name: str, **kwargs):
        """Update skill progress"""
        valid_fields = ['exercises_completed', 'exercises_correct', 'mastery_level',
                       'unlocked', 'last_practiced']
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        if not updates:
            return

        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE skill_progress SET {set_clause} WHERE skill_name = ?"
        with self.get_connection() as conn:
            conn.execute(query, tuple(updates.values()) + (skill_name,))

    def add_exercise_history(self, exercise_id: str, level: int, difficulty: str,
                            correct: bool, time_taken: int, user_query: str,
                            hints_used: int = 0, attempts: int = 1,
                            scenario: str = None):
        """Add an exercise attempt to history"""
        query = """
        INSERT INTO exercise_history
        (exercise_id, level, difficulty, scenario, correct, time_taken_seconds,
         user_query, hints_used, attempts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(query, (exercise_id, level, difficulty, scenario, correct,
                                time_taken, user_query, hints_used, attempts))

    def get_exercise_history(self, limit: int = 50) -> List[Dict]:
        """Get recent exercise history"""
        return self.execute(
            "SELECT * FROM exercise_history ORDER BY attempted_at DESC LIMIT ?",
            (limit,)
        )

    def get_achievements(self) -> List[Dict]:
        """Get all achievements"""
        return self.execute("SELECT * FROM achievements")

    def unlock_achievement(self, achievement_id: str, name: str, description: str):
        """Unlock an achievement"""
        query = """
        INSERT OR REPLACE INTO achievements
        (achievement_id, name, description, unlocked, unlocked_at)
        VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
        """
        with self.get_connection() as conn:
            conn.execute(query, (achievement_id, name, description))

    def get_setting(self, key: str, default: str = None) -> str:
        """Get a setting value"""
        result = self.execute("SELECT value FROM settings WHERE key = ?", (key,))
        return result[0]['value'] if result else default

    def set_setting(self, key: str, value: str):
        """Set a setting value"""
        query = "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)"
        with self.get_connection() as conn:
            conn.execute(query, (key, value))

    def get_stats_summary(self) -> Dict[str, Any]:
        """Get a comprehensive stats summary"""
        stats = self.get_user_stats()
        skills = self.get_skill_progress()
        achievements = self.get_achievements()

        # Calculate additional metrics
        history = self.execute("""
            SELECT level, difficulty, COUNT(*) as count,
                   SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count
            FROM exercise_history
            GROUP BY level, difficulty
        """)

        return {
            'user_stats': stats,
            'skills': skills,
            'achievements': [a for a in achievements if a['unlocked']],
            'history_summary': history,
            'total_unlocked_levels': sum(1 for s in skills if s['unlocked']),
            'overall_accuracy': (stats.get('total_correct', 0) / max(stats.get('total_exercises', 1), 1)) * 100
        }


class ExerciseDatabaseManager(DatabaseManager):
    """Manages the exercise data database (separate from user progress)"""

    def __init__(self):
        super().__init__(EXERCISE_DB_PATH)

    def execute_user_query(self, query: str, timeout: int = 10) -> Tuple[List[Dict], Optional[str]]:
        """
        Execute a user's query safely with timeout
        Returns (results, error_message)
        """
        try:
            with self.get_connection() as conn:
                conn.execute(f"PRAGMA busy_timeout = {timeout * 1000}")
                cursor = conn.execute(query)
                columns = [description[0] for description in cursor.description] if cursor.description else []
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results, None
        except sqlite3.Error as e:
            return [], str(e)
        except Exception as e:
            return [], f"Unexpected error: {str(e)}"

    def get_table_info(self, table_name: str) -> List[Dict]:
        """Get column information for a table"""
        return self.execute(f"PRAGMA table_info({table_name})")

    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict]:
        """Get sample data from a table"""
        try:
            return self.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
        except:
            return []

    def get_row_count(self, table_name: str) -> int:
        """Get the number of rows in a table"""
        try:
            result = self.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            return result[0]['count'] if result else 0
        except:
            return 0

    def get_all_tables(self) -> List[str]:
        """Get all table names in the database"""
        result = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [r['name'] for r in result]

    def get_schema_info(self) -> Dict[str, List[Dict]]:
        """Get complete schema information for all tables"""
        tables = self.get_all_tables()
        schema = {}
        for table in tables:
            schema[table] = {
                'columns': self.get_table_info(table),
                'row_count': self.get_row_count(table),
                'sample_data': self.get_sample_data(table)
            }
        return schema
