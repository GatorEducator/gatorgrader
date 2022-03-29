"""Tests for ListCheck's input and verification of command-line arguments."""

import os
import pytest
import sys

from unittest.mock import patch

from gator import arguments
from gator import report
from gator.exceptions import InvalidCheckArgumentsError
from gator.checks import check_ListChecks


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--namecontainsWRONG", "5"]),
        (["--namecontainsWRONG", "count_*"]),
        (["--namecontainsWRONG"]),
        (["--namecontains"]),
        (["CheckWrongName"]),
        (["ListChecksWrongName"]),
        (["ListChecksW"]),
    ],
)
def test_optional_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(InvalidCheckArgumentsError) as excinfo:
        _ = check_ListChecks.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output or error
    assert captured.err == ""
    assert captured.out == ""
    assert excinfo.value.check_name == "ListChecks"
    assert excinfo.value.usage
    assert excinfo.value.message


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        ([]),
        (["--namecontains", "check_"]),
        (["--namecontains", "commit", "--namecontains", "Count"]),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(InvalidCheckArgumentsError):
        _ = check_ListChecks.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "ListChecks"]),
        (["--json", "--nowelcome", "ListChecks"]),
        (["--nowelcome", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks", "--namecontains", "Com"]),
    ],
)
def test_act_produces_output(commandline_arguments, load_check):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # the result is True
        assert check_result is True
        # the report contains expected results
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is True
        assert report.get_result()["diagnostic"] == ""


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["ListChecks", "--namecontains", "NotValidCheckName"]),
        (
            [
                "--checkerdir",
                "./gator/checks",
                "ListChecks",
                "--namecontains",
                "NotValidCheckName",
            ]
        ),
    ],
)
def test_act_produces_output_invalid_check_name(commandline_arguments, load_check):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # the result is False
        assert check_result is False
        # the report contains expected results
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is False
        assert report.get_result()["diagnostic"] != ""
