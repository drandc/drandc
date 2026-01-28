"""
Result Comparator for SQL Practice Generator
Compares expected and actual query results
"""
from typing import List, Dict, Any, Tuple
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FLOATING_POINT_TOLERANCE


class ResultComparator:
    """Compares SQL query results"""

    class ComparisonResult:
        """Result of comparing two query results"""

        EXACT_MATCH = 'exact_match'
        CORRECT_UNORDERED = 'correct_unordered'
        PARTIALLY_CORRECT = 'partially_correct'
        COLUMN_MISMATCH = 'column_mismatch'
        WRONG_ROW_COUNT = 'wrong_row_count'
        WRONG_COLUMNS = 'wrong_columns'
        EMPTY_RESULT = 'empty_result'
        VALUE_MISMATCH = 'value_mismatch'

        STATUS_MESSAGES = {
            'exact_match': 'Correct! Results match exactly.',
            'correct_unordered': 'Correct! (Row order differs but results are correct)',
            'partially_correct': 'Partially correct - some values differ.',
            'column_mismatch': 'Column names differ from expected.',
            'wrong_row_count': 'Wrong number of rows returned.',
            'wrong_columns': 'Different columns than expected.',
            'empty_result': 'Query returned no rows (expected some).',
            'value_mismatch': 'Some values in the result are incorrect.'
        }

        def __init__(self, status: str, is_correct: bool, message: str,
                     details: Dict[str, Any] = None):
            self.status = status
            self.is_correct = is_correct
            self.message = message
            self.details = details or {}

        def to_dict(self) -> Dict[str, Any]:
            return {
                'status': self.status,
                'is_correct': self.is_correct,
                'message': self.message,
                'details': self.details
            }

    def __init__(self, case_sensitive: bool = False,
                 floating_tolerance: float = FLOATING_POINT_TOLERANCE,
                 order_matters: bool = True):
        """
        Initialize the comparator

        Args:
            case_sensitive: Whether string comparison is case-sensitive
            floating_tolerance: Tolerance for floating-point comparison
            order_matters: Whether row order matters
        """
        self.case_sensitive = case_sensitive
        self.floating_tolerance = floating_tolerance
        self.order_matters = order_matters

    def compare(self, expected: List[Dict], actual: List[Dict],
                order_required: bool = None) -> 'ResultComparator.ComparisonResult':
        """
        Compare expected and actual results

        Args:
            expected: Expected result rows
            actual: Actual result rows
            order_required: Override default order_matters setting

        Returns:
            ComparisonResult object
        """
        if order_required is None:
            order_required = self.order_matters

        # Check for empty results
        if not actual and expected:
            return self.ComparisonResult(
                self.ComparisonResult.EMPTY_RESULT,
                False,
                f"Query returned no rows (expected {len(expected)} rows).",
                {'expected_count': len(expected), 'actual_count': 0}
            )

        if not expected and actual:
            return self.ComparisonResult(
                self.ComparisonResult.WRONG_ROW_COUNT,
                False,
                f"Query returned {len(actual)} rows (expected 0 rows).",
                {'expected_count': 0, 'actual_count': len(actual)}
            )

        if not expected and not actual:
            return self.ComparisonResult(
                self.ComparisonResult.EXACT_MATCH,
                True,
                "Correct! Both queries returned empty results.",
                {'expected_count': 0, 'actual_count': 0}
            )

        # Check row count
        if len(expected) != len(actual):
            return self.ComparisonResult(
                self.ComparisonResult.WRONG_ROW_COUNT,
                False,
                f"Got {len(actual)} rows, expected {len(expected)} rows.",
                {'expected_count': len(expected), 'actual_count': len(actual)}
            )

        # Check columns
        expected_cols = set(expected[0].keys()) if expected else set()
        actual_cols = set(actual[0].keys()) if actual else set()

        if expected_cols != actual_cols:
            # Check if only case differs
            expected_lower = {c.lower() for c in expected_cols}
            actual_lower = {c.lower() for c in actual_cols}

            if expected_lower == actual_lower:
                # Column names differ only in case
                if self.case_sensitive:
                    return self.ComparisonResult(
                        self.ComparisonResult.COLUMN_MISMATCH,
                        False,
                        "Column names have different case than expected.",
                        {'expected_columns': list(expected_cols),
                         'actual_columns': list(actual_cols)}
                    )
                # Normalize column names and continue
                actual = self._normalize_column_names(actual, expected[0].keys())
            else:
                missing = expected_cols - actual_cols
                extra = actual_cols - expected_cols
                return self.ComparisonResult(
                    self.ComparisonResult.WRONG_COLUMNS,
                    False,
                    f"Different columns than expected. Missing: {missing or 'none'}, Extra: {extra or 'none'}",
                    {'expected_columns': list(expected_cols),
                     'actual_columns': list(actual_cols),
                     'missing': list(missing),
                     'extra': list(extra)}
                )

        # Compare values
        if order_required:
            # Ordered comparison
            return self._compare_ordered(expected, actual)
        else:
            # Unordered comparison
            return self._compare_unordered(expected, actual)

    def _compare_ordered(self, expected: List[Dict],
                        actual: List[Dict]) -> 'ResultComparator.ComparisonResult':
        """Compare results where order matters"""
        differences = []

        for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
            row_diff = self._compare_rows(exp_row, act_row)
            if row_diff:
                differences.append({
                    'row': i,
                    'differences': row_diff
                })

        if not differences:
            return self.ComparisonResult(
                self.ComparisonResult.EXACT_MATCH,
                True,
                "Correct! Results match exactly.",
                {'rows_compared': len(expected)}
            )

        # Check if unordered would match
        unordered_result = self._compare_unordered(expected, actual)
        if unordered_result.is_correct:
            return self.ComparisonResult(
                self.ComparisonResult.CORRECT_UNORDERED,
                True,
                "Correct! (Row order differs from expected, but all values are correct)",
                {'rows_compared': len(expected)}
            )

        return self.ComparisonResult(
            self.ComparisonResult.VALUE_MISMATCH,
            False,
            f"Found differences in {len(differences)} row(s).",
            {'differences': differences[:5],  # Limit to first 5
             'total_differences': len(differences)}
        )

    def _compare_unordered(self, expected: List[Dict],
                          actual: List[Dict]) -> 'ResultComparator.ComparisonResult':
        """Compare results where order doesn't matter"""
        # Convert to comparable format
        def row_to_tuple(row: Dict) -> tuple:
            items = []
            for k in sorted(row.keys()):
                v = row[k]
                if isinstance(v, float):
                    v = round(v, 6)
                elif isinstance(v, str) and not self.case_sensitive:
                    v = v.lower()
                items.append((k.lower() if not self.case_sensitive else k, v))
            return tuple(items)

        expected_set = set(row_to_tuple(r) for r in expected)
        actual_set = set(row_to_tuple(r) for r in actual)

        if expected_set == actual_set:
            return self.ComparisonResult(
                self.ComparisonResult.EXACT_MATCH,
                True,
                "Correct! Results match.",
                {'rows_compared': len(expected)}
            )

        missing = expected_set - actual_set
        extra = actual_set - expected_set

        if missing or extra:
            return self.ComparisonResult(
                self.ComparisonResult.VALUE_MISMATCH,
                False,
                f"Results differ. {len(missing)} expected rows missing, {len(extra)} unexpected rows.",
                {'missing_count': len(missing),
                 'extra_count': len(extra)}
            )

        return self.ComparisonResult(
            self.ComparisonResult.EXACT_MATCH,
            True,
            "Correct! Results match.",
            {}
        )

    def _compare_rows(self, expected: Dict, actual: Dict) -> List[Dict]:
        """Compare two rows and return differences"""
        differences = []

        for key in expected.keys():
            exp_val = expected[key]
            act_val = actual.get(key)

            if not self._values_equal(exp_val, act_val):
                differences.append({
                    'column': key,
                    'expected': exp_val,
                    'actual': act_val
                })

        return differences

    def _values_equal(self, expected, actual) -> bool:
        """Compare two values with appropriate tolerance"""
        if expected is None and actual is None:
            return True
        if expected is None or actual is None:
            return False

        # Float comparison with tolerance
        if isinstance(expected, float) and isinstance(actual, (int, float)):
            return abs(expected - float(actual)) <= self.floating_tolerance
        if isinstance(actual, float) and isinstance(expected, (int, float)):
            return abs(float(expected) - actual) <= self.floating_tolerance

        # String comparison
        if isinstance(expected, str) and isinstance(actual, str):
            exp_stripped = expected.strip()
            act_stripped = actual.strip()
            if self.case_sensitive:
                return exp_stripped == act_stripped
            return exp_stripped.lower() == act_stripped.lower()

        # Direct comparison
        return expected == actual

    def _normalize_column_names(self, rows: List[Dict],
                               target_names: List[str]) -> List[Dict]:
        """Normalize column names to match target"""
        if not rows:
            return rows

        # Create mapping from lowercase to target
        target_map = {name.lower(): name for name in target_names}

        result = []
        for row in rows:
            new_row = {}
            for key, value in row.items():
                target_key = target_map.get(key.lower(), key)
                new_row[target_key] = value
            result.append(new_row)

        return result

    def format_comparison_table(self, expected: List[Dict],
                               actual: List[Dict],
                               max_rows: int = 10) -> str:
        """Format a comparison table for display"""
        if not expected and not actual:
            return "Both results are empty."

        lines = []

        # Get columns
        all_cols = set()
        if expected:
            all_cols.update(expected[0].keys())
        if actual:
            all_cols.update(actual[0].keys())
        cols = sorted(all_cols)

        # Header
        header = "| " + " | ".join(f"{col:>15}" for col in cols) + " |"
        separator = "|" + "|".join("-" * 17 for _ in cols) + "|"

        lines.append("Expected:")
        lines.append(header)
        lines.append(separator)
        for row in expected[:max_rows]:
            row_str = "| " + " | ".join(
                f"{str(row.get(col, 'NULL')):>15}"[:15]
                for col in cols
            ) + " |"
            lines.append(row_str)
        if len(expected) > max_rows:
            lines.append(f"... and {len(expected) - max_rows} more rows")

        lines.append("")
        lines.append("Actual:")
        lines.append(header)
        lines.append(separator)
        for row in actual[:max_rows]:
            row_str = "| " + " | ".join(
                f"{str(row.get(col, 'NULL')):>15}"[:15]
                for col in cols
            ) + " |"
            lines.append(row_str)
        if len(actual) > max_rows:
            lines.append(f"... and {len(actual) - max_rows} more rows")

        return "\n".join(lines)


def compare_results(expected: List[Dict], actual: List[Dict],
                   case_sensitive: bool = False,
                   order_matters: bool = True) -> Dict[str, Any]:
    """
    Convenience function to compare query results

    Args:
        expected: Expected result rows
        actual: Actual result rows
        case_sensitive: Whether string comparison is case-sensitive
        order_matters: Whether row order matters

    Returns:
        Dictionary with comparison results
    """
    comparator = ResultComparator(
        case_sensitive=case_sensitive,
        order_matters=order_matters
    )
    result = comparator.compare(expected, actual)
    return result.to_dict()
