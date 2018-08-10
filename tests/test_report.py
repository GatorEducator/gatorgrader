"""Test cases for the report module"""

import pytest

from gator import report


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary"""
    report.reset()


def test_create_result():
    """Create a result dictionary and check for the correct form"""
    new_result = report.create_result("Command executes", True, "")
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_add_single_result_to_report(reset_results_dictionary):
    """Add a single row to the report and check for containment"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_add_multiple_results_to_report(reset_results_dictionary):
    """Add multiple row to the report and check for containment"""
    identifier, new_result = report.add_result("Command executes", True, "")
    # create the first result and add it to the report dictionary
    assert identifier == 0
    assert new_result is not None
    assert isinstance(new_result, dict) is True
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""
    # create the second result and add it to the report dictionary
    identifier_next, new_result_next = report.add_result(
        "Check for 3 paragraphs", False, "Only found 2 paragraphs"
    )
    assert identifier_next == 1
    assert new_result_next is not None
    assert isinstance(new_result_next, dict) is True
    assert len(new_result_next) == 3
    assert report.get_size() == 2
    assert new_result_next[report.CHECK] == "Check for 3 paragraphs"
    assert new_result_next[report.OUTCOME] is False
    assert new_result_next[report.DIAGNOSTIC] == "Only found 2 paragraphs"
    assert isinstance(report.get_details(), dict) is True
