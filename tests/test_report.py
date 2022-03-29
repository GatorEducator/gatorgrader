"""Test cases for the report module."""

import pytest

from gator import constants
from gator import report


def test_create_result():
    """Create a result dictionary and check for the correct form."""
    new_result = report.create_result("Command executes", True, "")
    assert new_result[constants.results.Description] == "Command executes"
    assert new_result[constants.results.Outcome] is True
    assert new_result[constants.results.Diagnostic] == ""


# pylint: disable=unused-argument
def test_set_result(reset_results_dictionary):
    """Set the result dictionary and check if it keeps the values."""
    report.set_result("Command executes", True, "")
    assert report.get_result()[constants.results.Description] == "Command executes"
    assert report.get_result()[constants.results.Outcome] is True
    assert report.get_result()[constants.results.Diagnostic] == ""


# pylint: disable=unused-argument
def test_set_result_return(reset_results_dictionary):
    """Set the result dictionary and check if it keeps the values."""
    new_result = report.set_result("Command executes", False, "Missing trailing slash")
    assert new_result[constants.results.Description] == "Command executes"
    assert new_result[constants.results.Outcome] is False
    assert new_result[constants.results.Diagnostic] == "Missing trailing slash"


# pylint: disable=unused-argument
def test_output_text(reset_results_dictionary):
    """Set the report and check the textual output."""
    report.set_result("Command executes", True, "")
    output = report.output(report.get_result(), report.TEXT)
    assert "Command executes" in output
    assert "\n" not in output


# pylint: disable=unused-argument
def test_output_text_diagnostic(reset_results_dictionary):
    """Set the report and check the textual output."""
    report.set_result("Command executes", False, "Missing trailing slash")
    output = report.output(report.get_result(), report.TEXT)
    assert "Command executes" in output
    assert "Missing trailing slash" in output
    assert "\n" in output


# pylint: disable=unused-argument
def test_output_json(reset_results_dictionary):
    """Set the report and check output as JSON-based text."""
    report.set_result("Command executes", True, "")
    output = report.output(report.get_result(), report.JSON)
    assert output is not None
    assert "\n" not in output
    assert "Command executes" in output
    assert "true" in output
    assert f'"{constants.results.Description}":' in output
    assert f'"{constants.results.Outcome}":' in output
    assert f'"{constants.results.Diagnostic}":' in output
