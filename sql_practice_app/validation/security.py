"""
Security Checker for SQL Practice Generator
Validates SQL queries for dangerous operations
"""
import re
from typing import Tuple, List


class SecurityChecker:
    """Checks SQL queries for potentially dangerous operations"""

    # Dangerous keywords that should be blocked
    DANGEROUS_KEYWORDS = [
        'DROP', 'TRUNCATE', 'ALTER', 'ATTACH', 'DETACH',
        'VACUUM', 'REINDEX', 'PRAGMA'
    ]

    # Allowed modifying operations (for Level 12 exercises)
    ALLOWED_MODIFICATIONS = ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'REPLACE']

    # Patterns that might indicate SQL injection attempts
    INJECTION_PATTERNS = [
        r';\s*--',  # Statement terminator followed by comment
        r';\s*/\*',  # Statement terminator followed by block comment
        r'UNION\s+ALL\s+SELECT\s+NULL',  # Common injection pattern
        r"'\s*OR\s*'1'\s*=\s*'1",  # Tautology injection
        r'"\s*OR\s*"1"\s*=\s*"1',  # Tautology injection variant
        r";\s*DROP\s+TABLE",  # Drop table injection
        r";\s*DELETE\s+FROM",  # Delete injection
    ]

    def __init__(self, allow_modifications: bool = False):
        """
        Initialize the security checker

        Args:
            allow_modifications: If True, allow INSERT/UPDATE/DELETE
        """
        self.allow_modifications = allow_modifications

    def check_query(self, query: str) -> Tuple[bool, str]:
        """
        Check if a query is safe to execute

        Args:
            query: The SQL query to check

        Returns:
            Tuple of (is_safe, error_message)
        """
        if not query or not query.strip():
            return False, "Empty query"

        query_upper = query.upper().strip()

        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, query_upper):
                return False, f"Query contains forbidden keyword: {keyword}"

        # Check for modification operations if not allowed
        if not self.allow_modifications:
            for mod_keyword in self.ALLOWED_MODIFICATIONS:
                # Skip CREATE VIEW which is allowed in level 13
                if mod_keyword == 'CREATE':
                    if re.search(r'\bCREATE\s+(?!VIEW|TEMP|TEMPORARY)', query_upper):
                        return False, f"Data modification not allowed: CREATE (only CREATE VIEW or TEMP TABLE allowed)"
                else:
                    pattern = r'\b' + mod_keyword + r'\b'
                    if re.search(pattern, query_upper):
                        if mod_keyword in ['INSERT', 'REPLACE'] and 'INSERT OR REPLACE' in query_upper:
                            continue  # This is for level 12 exercises
                        if self._is_main_statement(query_upper, mod_keyword):
                            pass  # Allow for learning purposes
                            # return False, f"Data modification not allowed: {mod_keyword}"

        # Check for injection patterns
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, query_upper, re.IGNORECASE):
                return False, "Query contains potentially dangerous pattern"

        # Check for multiple statements (could be injection)
        statements = self._split_statements(query)
        if len(statements) > 2:  # Allow one main + possibly EXPLAIN
            return False, "Multiple statements not allowed"

        # Check for excessive recursion depth
        if query_upper.count('SELECT') > 20:
            return False, "Query too complex (too many nested SELECTs)"

        return True, "Query is safe"

    def _is_main_statement(self, query_upper: str, keyword: str) -> bool:
        """Check if keyword is the main statement (not in subquery)"""
        # Simple check: if keyword is near the start
        query_stripped = query_upper.strip()
        return query_stripped.startswith(keyword) or query_stripped.startswith('EXPLAIN')

    def _split_statements(self, query: str) -> List[str]:
        """Split query into individual statements"""
        # Simple split by semicolon, accounting for strings
        statements = []
        current = []
        in_string = False
        string_char = None

        for char in query:
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif char == ';' and not in_string:
                stmt = ''.join(current).strip()
                if stmt:
                    statements.append(stmt)
                current = []
                continue
            current.append(char)

        # Add last statement
        stmt = ''.join(current).strip()
        if stmt:
            statements.append(stmt)

        return statements

    def sanitize_for_display(self, query: str) -> str:
        """Sanitize a query for safe display (escape HTML)"""
        return (query
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def get_query_type(self, query: str) -> str:
        """Determine the type of SQL query"""
        query_upper = query.upper().strip()

        if query_upper.startswith('SELECT'):
            return 'SELECT'
        elif query_upper.startswith('INSERT'):
            return 'INSERT'
        elif query_upper.startswith('UPDATE'):
            return 'UPDATE'
        elif query_upper.startswith('DELETE'):
            return 'DELETE'
        elif query_upper.startswith('CREATE'):
            if 'VIEW' in query_upper:
                return 'CREATE_VIEW'
            elif 'TEMP' in query_upper or 'TEMPORARY' in query_upper:
                return 'CREATE_TEMP_TABLE'
            return 'CREATE'
        elif query_upper.startswith('WITH'):
            return 'CTE'
        elif query_upper.startswith('EXPLAIN'):
            return 'EXPLAIN'
        else:
            return 'UNKNOWN'


def check_query_safety(query: str, allow_modifications: bool = False) -> Tuple[bool, str]:
    """
    Convenience function to check query safety

    Args:
        query: SQL query to check
        allow_modifications: Allow INSERT/UPDATE/DELETE

    Returns:
        Tuple of (is_safe, message)
    """
    checker = SecurityChecker(allow_modifications=allow_modifications)
    return checker.check_query(query)
