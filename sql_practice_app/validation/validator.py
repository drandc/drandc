"""
Query Validator for SQL Practice Generator
Main validation engine for user queries
"""
import sqlite3
import time
import re
from typing import Dict, Any, List, Tuple, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import QUERY_TIMEOUT, MAX_RESULT_ROWS, EXERCISE_DB_PATH
from validation.security import SecurityChecker
from validation.comparator import ResultComparator


class QueryValidator:
    """Validates user SQL queries against expected solutions"""

    # Common error patterns and helpful hints
    ERROR_HINTS = {
        r'no such table': "Check the table name - it might be misspelled or doesn't exist in this database.",
        r'no such column': "Check the column name - it might be misspelled or doesn't exist in this table.",
        r'ambiguous column': "This column exists in multiple tables. Use table_name.column_name to specify which one.",
        r'near "([^"]+)"': "Syntax error near '{0}'. Check for missing keywords, commas, or parentheses.",
        r'syntax error': "There's a syntax error in your query. Check for typos, missing keywords, or incorrect order of clauses.",
        r'not an aggregate': "You're using a non-aggregated column with aggregate functions. Add it to GROUP BY or use an aggregate function.",
        r'HAVING clause': "HAVING is used with GROUP BY to filter groups. Make sure you have a GROUP BY clause.",
        r'ORDER BY term': "The ORDER BY column doesn't exist in your SELECT. Either select it or use a column alias.",
        r'misuse of aggregate': "Aggregate functions (COUNT, SUM, AVG, etc.) can't be used in WHERE. Use HAVING instead.",
        r'GROUP BY clause': "When using GROUP BY, SELECT can only contain grouped columns or aggregate functions.",
        r'recursive': "Recursive queries require WITH RECURSIVE keyword and proper base case + recursive case.",
    }

    def __init__(self, db_path: str = EXERCISE_DB_PATH):
        """
        Initialize the validator

        Args:
            db_path: Path to the exercise database
        """
        self.db_path = db_path
        self.security = SecurityChecker()
        self.comparator = ResultComparator()

    def validate(self, user_query: str, expected_query: str,
                exercise: Dict = None) -> Dict[str, Any]:
        """
        Validate a user's query against the expected solution

        Args:
            user_query: The user's SQL query
            expected_query: The expected solution query
            exercise: Exercise metadata (optional)

        Returns:
            Validation result dictionary
        """
        start_time = time.time()
        result = {
            'is_correct': False,
            'status': 'unknown',
            'message': '',
            'user_results': [],
            'expected_results': [],
            'execution_time': 0,
            'hints': [],
            'details': {}
        }

        # Step 1: Security check
        is_safe, security_msg = self.security.check_query(user_query)
        if not is_safe:
            result['status'] = 'security_error'
            result['message'] = f"Security check failed: {security_msg}"
            return result

        # Step 2: Syntax validation (try to parse)
        syntax_error = self._check_syntax(user_query)
        if syntax_error:
            result['status'] = 'syntax_error'
            result['message'] = f"Syntax error: {syntax_error}"
            result['hints'] = self._get_error_hints(syntax_error)
            return result

        # Step 3: Execute both queries
        user_results, user_error = self._execute_query(user_query)
        if user_error:
            result['status'] = 'execution_error'
            result['message'] = f"Execution error: {user_error}"
            result['hints'] = self._get_error_hints(user_error)
            return result

        expected_results, expected_error = self._execute_query(expected_query)
        if expected_error:
            result['status'] = 'internal_error'
            result['message'] = "Error executing expected query (this is a bug)"
            result['details']['expected_error'] = expected_error
            return result

        # Step 4: Compare results
        result['user_results'] = user_results[:MAX_RESULT_ROWS]
        result['expected_results'] = expected_results[:MAX_RESULT_ROWS]
        result['execution_time'] = round(time.time() - start_time, 3)

        # Determine if order matters based on exercise
        order_matters = self._should_check_order(user_query, expected_query, exercise)

        comparison = self.comparator.compare(
            expected_results,
            user_results,
            order_required=order_matters
        )

        result['is_correct'] = comparison.is_correct
        result['status'] = comparison.status
        result['message'] = comparison.message
        result['details'] = comparison.details

        # Add performance warning if slow
        if result['execution_time'] > 5:
            result['hints'].append("Your query took over 5 seconds. Consider optimizing it.")

        # Add common mistake hints for incorrect answers
        if not result['is_correct']:
            result['hints'].extend(self._get_mistake_hints(
                user_query, expected_query, user_results, expected_results
            ))

        return result

    def _check_syntax(self, query: str) -> Optional[str]:
        """Check query syntax without executing"""
        try:
            conn = sqlite3.connect(':memory:')
            # Use EXPLAIN to check syntax without full execution
            conn.execute(f"EXPLAIN {query}")
            conn.close()
            return None
        except sqlite3.Error as e:
            return str(e)
        except Exception as e:
            return str(e)

    def _execute_query(self, query: str) -> Tuple[List[Dict], Optional[str]]:
        """Execute a query and return results or error"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute(f"PRAGMA busy_timeout = {QUERY_TIMEOUT * 1000}")

            # Handle EXPLAIN queries specially
            if query.strip().upper().startswith('EXPLAIN'):
                cursor = conn.execute(query)
            else:
                cursor = conn.execute(query)

            if cursor.description:
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]
            else:
                results = []

            conn.close()
            return results, None

        except sqlite3.OperationalError as e:
            return [], str(e)
        except sqlite3.Error as e:
            return [], str(e)
        except Exception as e:
            return [], f"Unexpected error: {str(e)}"

    def _should_check_order(self, user_query: str, expected_query: str,
                           exercise: Dict = None) -> bool:
        """Determine if row order should be checked"""
        # If expected query has ORDER BY, order matters
        if re.search(r'\bORDER\s+BY\b', expected_query, re.IGNORECASE):
            return True

        # If exercise specifies
        if exercise and exercise.get('order_matters'):
            return True

        # Otherwise, order doesn't matter
        return False

    def _get_error_hints(self, error_message: str) -> List[str]:
        """Get helpful hints based on error message"""
        hints = []
        error_lower = error_message.lower()

        for pattern, hint in self.ERROR_HINTS.items():
            match = re.search(pattern, error_message, re.IGNORECASE)
            if match:
                # Format hint with matched groups if any
                if match.groups():
                    hints.append(hint.format(*match.groups()))
                else:
                    hints.append(hint)

        if not hints:
            hints.append("Check your SQL syntax carefully. Common issues include missing commas, unclosed quotes, or incorrect keyword order.")

        return hints

    def _get_mistake_hints(self, user_query: str, expected_query: str,
                          user_results: List[Dict],
                          expected_results: List[Dict]) -> List[str]:
        """Generate hints for common mistakes"""
        hints = []
        user_upper = user_query.upper()
        expected_upper = expected_query.upper()

        # Check for missing GROUP BY
        if 'GROUP BY' in expected_upper and 'GROUP BY' not in user_upper:
            if any(agg in expected_upper for agg in ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX']):
                hints.append("Did you forget to use GROUP BY? The expected solution groups the results.")

        # Check for missing aggregation
        if any(agg in expected_upper for agg in ['COUNT(', 'SUM(', 'AVG(']):
            if not any(agg in user_upper for agg in ['COUNT(', 'SUM(', 'AVG(']):
                hints.append("The expected solution uses aggregate functions (COUNT, SUM, AVG). Did you aggregate your data?")

        # Check for missing JOIN
        if 'JOIN' in expected_upper and 'JOIN' not in user_upper:
            hints.append("The expected solution uses a JOIN to combine tables. Check if you need to join tables.")

        # Check for missing WHERE
        if 'WHERE' in expected_upper and 'WHERE' not in user_upper:
            hints.append("The expected solution filters rows with WHERE. Did you add the necessary filter conditions?")

        # Check for missing HAVING
        if 'HAVING' in expected_upper and 'HAVING' not in user_upper:
            hints.append("The expected solution uses HAVING to filter groups. Did you add HAVING after GROUP BY?")

        # Check row count difference
        if user_results and expected_results:
            if len(user_results) > len(expected_results) * 2:
                hints.append("Your query returned too many rows. Check your WHERE or HAVING conditions.")
            elif len(user_results) < len(expected_results) / 2:
                hints.append("Your query returned too few rows. Your conditions might be too restrictive.")

        # Check for Cartesian product (too many results)
        if user_results and len(user_results) > 10000:
            hints.append("Your query returned a very large number of rows. Did you forget a JOIN condition?")

        # Check for missing ORDER BY when order differs
        if expected_results and user_results:
            if 'ORDER BY' in expected_upper and 'ORDER BY' not in user_upper:
                hints.append("The expected solution uses ORDER BY. Add ORDER BY to sort your results.")

        return hints[:3]  # Limit hints to avoid overwhelming

    def get_schema_info(self, tables: List[str] = None) -> Dict[str, Any]:
        """Get schema information for specified tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get all tables if not specified
            if not tables:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                tables = [row[0] for row in cursor.fetchall()]

            schema = {}
            for table in tables:
                # Get column info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = []
                for row in cursor.fetchall():
                    columns.append({
                        'name': row[1],
                        'type': row[2],
                        'nullable': not row[3],
                        'primary_key': bool(row[5])
                    })

                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]

                # Get sample data
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                col_names = [desc[0] for desc in cursor.description]
                sample_data = [dict(zip(col_names, row)) for row in cursor.fetchall()]

                schema[table] = {
                    'columns': columns,
                    'row_count': row_count,
                    'sample_data': sample_data
                }

            conn.close()
            return schema

        except sqlite3.Error as e:
            return {'error': str(e)}

    def execute_playground_query(self, query: str) -> Dict[str, Any]:
        """Execute a query in playground mode (no validation)"""
        start_time = time.time()

        # Security check
        is_safe, security_msg = self.security.check_query(query)
        if not is_safe:
            return {
                'success': False,
                'error': f"Security check failed: {security_msg}",
                'results': [],
                'execution_time': 0
            }

        # Execute
        results, error = self._execute_query(query)
        execution_time = round(time.time() - start_time, 3)

        if error:
            return {
                'success': False,
                'error': error,
                'hints': self._get_error_hints(error),
                'results': [],
                'execution_time': execution_time
            }

        return {
            'success': True,
            'results': results[:MAX_RESULT_ROWS],
            'row_count': len(results),
            'truncated': len(results) > MAX_RESULT_ROWS,
            'execution_time': execution_time
        }


class ValidationEngine:
    """High-level validation engine for exercise validation"""

    def __init__(self):
        self.validator = QueryValidator()

    def validate_exercise(self, user_query: str, exercise: Dict) -> Dict[str, Any]:
        """
        Validate a user's answer to an exercise

        Args:
            user_query: The user's SQL query
            exercise: The exercise dictionary with solution

        Returns:
            Comprehensive validation result
        """
        if 'solution' not in exercise:
            return {
                'is_correct': False,
                'status': 'internal_error',
                'message': 'Exercise has no solution defined'
            }

        result = self.validator.validate(
            user_query,
            exercise['solution'],
            exercise
        )

        # Add exercise context to result
        result['exercise_id'] = exercise.get('id', 'unknown')
        result['level'] = exercise.get('level', 0)
        result['difficulty'] = exercise.get('difficulty', 'unknown')

        return result

    def get_exercise_hints(self, exercise: Dict, hint_level: int = 1) -> List[str]:
        """
        Get progressive hints for an exercise

        Args:
            exercise: The exercise dictionary
            hint_level: 1-3, with 3 being most revealing

        Returns:
            List of hints up to the requested level
        """
        hints = exercise.get('hints', [])
        return hints[:min(hint_level, len(hints))]

    def get_solution_explanation(self, exercise: Dict) -> Dict[str, Any]:
        """
        Get the solution with explanation

        Args:
            exercise: The exercise dictionary

        Returns:
            Solution and explanation
        """
        return {
            'solution': exercise.get('solution', ''),
            'explanation': exercise.get('explanation', 'No explanation available.'),
            'key_concepts': exercise.get('skills', [])
        }
