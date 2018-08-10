"""Test cases for the report module"""

from gator import report


def test_add_single_row_to_report():
    """Add a single row to the report and check for containment"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
