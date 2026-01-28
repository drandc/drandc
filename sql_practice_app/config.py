"""
Configuration settings for SQL Practice Generator
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database settings
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'sql_practice.db')
EXERCISE_DB_PATH = os.path.join(BASE_DIR, 'data', 'exercise_data.db')

# Ensure data directory exists
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

# Application settings
SECRET_KEY = 'sql-practice-generator-secret-key-change-in-production'
DEBUG = True

# Query execution settings
QUERY_TIMEOUT = 10  # seconds
MAX_RESULT_ROWS = 1000
FLOATING_POINT_TOLERANCE = 0.01

# Validation settings
VALIDATION_STRICTNESS = 'relaxed'  # 'strict' or 'relaxed'
CASE_SENSITIVE = False
AUTO_ADVANCE = False

# Progression settings
UNLOCK_THRESHOLD = 10  # exercises needed to unlock next level
UNLOCK_SUCCESS_RATE = 0.70  # 70% success rate required

# Skill levels definition
SKILL_LEVELS = {
    1: {
        'name': 'Foundation',
        'description': 'SELECT, WHERE, basic operators (=, >, <, BETWEEN, IN, LIKE), LIMIT/OFFSET',
        'skills': ['SELECT', 'WHERE', 'OPERATORS', 'BETWEEN', 'IN', 'LIKE', 'LIMIT', 'OFFSET'],
        'prerequisites': []
    },
    2: {
        'name': 'Sorting & Uniqueness',
        'description': 'ORDER BY, DISTINCT, basic string/math functions',
        'skills': ['ORDER_BY', 'DISTINCT', 'UPPER', 'LOWER', 'ROUND', 'ABS', 'LENGTH', 'SUBSTR'],
        'prerequisites': [1]
    },
    3: {
        'name': 'Aggregation Basics',
        'description': 'GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX',
        'skills': ['GROUP_BY', 'HAVING', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX'],
        'prerequisites': [1, 2]
    },
    4: {
        'name': 'Basic Joins',
        'description': 'INNER JOIN, table aliases, understanding join conditions',
        'skills': ['INNER_JOIN', 'TABLE_ALIAS', 'JOIN_CONDITIONS'],
        'prerequisites': [1, 2, 3]
    },
    5: {
        'name': 'Advanced Joins',
        'description': 'LEFT/RIGHT/FULL OUTER JOINs, self-joins, multiple table joins, CROSS JOIN',
        'skills': ['LEFT_JOIN', 'RIGHT_JOIN', 'FULL_JOIN', 'SELF_JOIN', 'MULTIPLE_JOINS', 'CROSS_JOIN'],
        'prerequisites': [1, 2, 3, 4]
    },
    6: {
        'name': 'Subqueries',
        'description': 'Subqueries in WHERE, FROM (derived tables), SELECT, correlated subqueries, EXISTS/NOT EXISTS',
        'skills': ['SUBQUERY_WHERE', 'SUBQUERY_FROM', 'SUBQUERY_SELECT', 'CORRELATED_SUBQUERY', 'EXISTS', 'NOT_EXISTS'],
        'prerequisites': [1, 2, 3, 4, 5]
    },
    7: {
        'name': 'Conditional Logic',
        'description': 'CASE statements, COALESCE, NULLIF, IIF',
        'skills': ['CASE', 'COALESCE', 'NULLIF', 'IIF'],
        'prerequisites': [1, 2, 3, 4, 5, 6]
    },
    8: {
        'name': 'Window Functions',
        'description': 'ROW_NUMBER, RANK, DENSE_RANK, NTILE, LAG, LEAD, FIRST_VALUE, LAST_VALUE, SUM/AVG OVER',
        'skills': ['ROW_NUMBER', 'RANK', 'DENSE_RANK', 'NTILE', 'LAG', 'LEAD', 'FIRST_VALUE', 'LAST_VALUE', 'WINDOW_AGGREGATE'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7]
    },
    9: {
        'name': 'CTEs',
        'description': 'WITH clause, multiple CTEs, chaining CTEs',
        'skills': ['CTE_BASIC', 'CTE_MULTIPLE', 'CTE_CHAINED'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7, 8]
    },
    10: {
        'name': 'Advanced CTEs',
        'description': 'Recursive CTEs, complex multi-level CTEs with window functions',
        'skills': ['CTE_RECURSIVE', 'CTE_COMPLEX'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    11: {
        'name': 'Optimization',
        'description': 'EXPLAIN/EXPLAIN QUERY PLAN, index usage, query performance analysis',
        'skills': ['EXPLAIN', 'EXPLAIN_QUERY_PLAN', 'INDEX_USAGE', 'PERFORMANCE_ANALYSIS'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    12: {
        'name': 'Data Manipulation',
        'description': 'INSERT, UPDATE, DELETE with complex WHERE clauses, UPSERT/INSERT OR REPLACE',
        'skills': ['INSERT', 'UPDATE', 'DELETE', 'UPSERT', 'INSERT_OR_REPLACE'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    },
    13: {
        'name': 'Advanced Topics',
        'description': 'Transactions, CREATE VIEW, temporary tables, date/time mastery',
        'skills': ['TRANSACTION', 'CREATE_VIEW', 'TEMP_TABLE', 'DATETIME_FUNCTIONS'],
        'prerequisites': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
}

# Difficulty settings
DIFFICULTY_LEVELS = {
    'easy': {
        'prereq_skills': (1, 2),
        'description': 'Core concept + 1-2 prerequisite skills'
    },
    'medium': {
        'prereq_skills': (3, 4),
        'description': 'Core concept + 3-4 prerequisite skills + moderate complexity'
    },
    'hard': {
        'prereq_skills': (5, 10),
        'description': 'Core concept + 5+ prerequisite skills + real-world complexity + edge cases'
    }
}

# Mastery levels
MASTERY_LEVELS = {
    'none': 0,
    'bronze': 10,
    'silver': 25,
    'gold': 50,
    'platinum': 100
}

# Achievement definitions
ACHIEVEMENTS = {
    'first_steps': {
        'name': 'First Steps',
        'description': 'Complete your first exercise',
        'icon': 'trophy',
        'condition': 'total_exercises >= 1'
    },
    'perfectionist': {
        'name': 'Perfectionist',
        'description': '10 exercises in a row correct',
        'icon': 'star',
        'condition': 'current_streak >= 10'
    },
    'speed_demon': {
        'name': 'Speed Demon',
        'description': 'Complete exercise in under 60 seconds',
        'icon': 'lightning',
        'condition': 'fastest_time < 60'
    },
    'persistent': {
        'name': 'Persistent',
        'description': 'Solve after 3+ attempts',
        'icon': 'shield',
        'condition': 'solved_after_attempts >= 3'
    },
    'diverse_learner': {
        'name': 'Diverse Learner',
        'description': 'Practice all skill levels in one week',
        'icon': 'book',
        'condition': 'weekly_levels >= 13'
    },
    'sql_master': {
        'name': 'SQL Master',
        'description': 'Complete 500 total exercises',
        'icon': 'crown',
        'condition': 'total_exercises >= 500'
    },
    'century': {
        'name': 'Century',
        'description': 'Complete 100 exercises',
        'icon': 'medal',
        'condition': 'total_exercises >= 100'
    },
    'week_warrior': {
        'name': 'Week Warrior',
        'description': '7-day practice streak',
        'icon': 'fire',
        'condition': 'day_streak >= 7'
    },
    'join_master': {
        'name': 'Join Master',
        'description': 'Complete 20 join exercises',
        'icon': 'link',
        'condition': 'join_exercises >= 20'
    },
    'aggregation_pro': {
        'name': 'Aggregation Pro',
        'description': 'Complete 20 aggregation exercises',
        'icon': 'calculator',
        'condition': 'aggregation_exercises >= 20'
    }
}

# Data scenarios
DATA_SCENARIOS = ['ecommerce', 'hr', 'finance', 'social_media', 'healthcare', 'education']
