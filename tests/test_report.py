"""Test cases for the report module"""

from gator import report


def test_create_result():
    """Create a result dictionary and check for the correct form"""
    new_result = report.create_result("Command executes", True, "")
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""


def test_add_single_result_to_report():
    """Add a single row to the report and check for containment"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""
