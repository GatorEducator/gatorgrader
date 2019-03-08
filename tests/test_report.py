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
def test_set_result(reset_results_dictionary):
    """Set the result dictionary and check if it keeps the values"""
    report.set_result("Command executes", True, "")
    assert report.get_result()[report.CHECK] == "Command executes"
    assert report.get_result()[report.OUTCOME] is True
    assert report.get_result()[report.DIAGNOSTIC] == ""


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_set_result_return(reset_results_dictionary):
    """Set the result dictionary and check if it keeps the values"""
    new_result = report.set_result("Command executes", False, "Missing trailing slash")
    assert new_result[report.CHECK] == "Command executes"
    assert new_result[report.OUTCOME] is False
    assert new_result[report.DIAGNOSTIC] == "Missing trailing slash"


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_output_text(reset_results_dictionary):
    """Set the report and check the textual output"""
    report.set_result("Command executes", True, "")
    output = report.output(report.get_result(), report.TEXT)
    assert "Command executes" in output
    assert "\n" not in output


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_output_text_diagnostic(reset_results_dictionary):
    """Set the report and check the textual output"""
    report.set_result("Command executes", False, "Missing trailing slash")
    output = report.output(report.get_result(), report.TEXT)
    assert "Command executes" in output
    assert "Missing trailing slash" in output
    assert "\n" in output


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_output_json(reset_results_dictionary):
    """Set the report and check output as JSON-based text"""
    report.set_result("Command executes", True, "")
    output = report.output(report.get_result(), report.JSON)
    assert output is not None
    assert "\n" not in output
    assert "Command executes" in output
    assert "true" in output
    assert f'"{report.CHECK}":' in output
    assert f'"{report.OUTCOME}":' in output
    assert f'"{report.DIAGNOSTIC}":' in output

