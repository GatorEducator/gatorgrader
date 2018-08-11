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


def test_dictionary_is_not_nested():
    """Check to see if a dictionary contains a nested one or not"""
    new_result = report.create_result("Command executes", True, "")
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""
    assert report.contains_nested_dictionary(new_result) is False


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_dictionary_is_nested(reset_results_dictionary):
    """Add a single row to the report and check for containment"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert report.contains_nested_dictionary(new_result) is False
    assert report.contains_nested_dictionary(report.get_details()) is True


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
def test_add_single_result_to_report_check_detail(reset_results_dictionary):
    """Add a single row to the report and check get_detail"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""
    assert report.get_detail(0) is not None


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


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_add_single_result_to_report_check_text_output(reset_results_dictionary):
    """Add a single row to the report and check the textual output"""
    identifier, new_result = report.add_result("Command executes", True, "")
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is True
    assert new_result[report.DIAGNOSTIC] == ""
    output_list = []
    report.output_text(new_result, output_list)
    assert len(output_list) == 1
    assert "\n" not in output_list[0]


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_add_single_result_to_report_check_text_output_diagnostic(
    reset_results_dictionary
):
    """Add a single row to the report and check the textual output"""
    identifier, new_result = report.add_result(
        "Command executes", False, "Missing trailing slash"
    )
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is False
    assert new_result[report.DIAGNOSTIC] == "Missing trailing slash"
    output_list = []
    report.output_text(new_result, output_list)
    assert len(output_list) == 1
    assert "\n" in output_list[0]


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_add_single_result_to_report_check_text_output_diagnostic_nested(
    reset_results_dictionary
):
    """Add a single row to the report and check the textual output"""
    identifier, new_result = report.add_result(
        "Command executes", False, "Missing trailing slash"
    )
    assert identifier == 0
    assert new_result is not None
    assert len(new_result) == 3
    assert report.get_size() == 1
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is False
    assert new_result[report.DIAGNOSTIC] == "Missing trailing slash"
    output_list = []
    report.output_text(report.get_details(), output_list)
    assert len(output_list) == 1
    assert "\n" in output_list[0]


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_output_text(reset_results_dictionary):
    """Add multiple row to the report and check final output as list-based text"""
    report.add_result("Command executes", True, "")
    report.add_result("Check for 3 paragraphs", False, "Only found 2 paragraphs")
    report.add_result("Check for 10 comments", True, "Only found 2 comments")
    output_list = report.output(report.get_details(), report.TEXT)
    assert len(output_list) == 3
    output = "\n".join(output_list)
    assert output is not None
    assert "\n" in output
    print(output)


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_output_json(reset_results_dictionary):
    """Add multiple row to the report and check final output as JSON-based text"""
    report.add_result("Command executes", True, "")
    report.add_result("Check for 3 paragraphs", False, "Only found 2 paragraphs")
    report.add_result("Check for 10 comments", True, "Only found 2 comments")
    output_list = report.output(report.get_details(), report.JSON)
    assert len(output_list) == 1
    output = " ".join(output_list)
    assert output is not None
    assert "\n" not in output
