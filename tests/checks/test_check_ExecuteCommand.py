"""Tests for ExecuteCommand's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch


from gator import arguments
from gator import report
from gator.exceptions import InvalidCheckArgumentsError
from gator.checks import check_ExecuteCommand


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        ([]),
        (["--commandWRONG", "echo"]),
        (["--command", "run", "--WRONG"]),
        (["--command"]),
    ],
)
def test_required_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(InvalidCheckArgumentsError) as excinfo:
        _ = check_ExecuteCommand.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output or error
    assert captured.err == ""
    assert captured.out == ""
    assert excinfo.value.check_name == "ExecuteCommand"
    assert excinfo.value.usage
    assert excinfo.value.error


@pytest.mark.parametrize(
    "commandline_arguments",
    [(["--command", "run_command_first"]), (["--command", "run_command_second"])],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(InvalidCheckArgumentsError):
        _ = check_ExecuteCommand.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments, expected_result",
    [
        (["ExecuteCommand", "--command", "WrongCommand"], False),
        (["ExecuteCommand", "--command", 'echo "CorrectCommand"'], True),
    ],
)
def test_act_produces_output(commandline_arguments, expected_result, load_check):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is expected_result
        # check the contents of the report
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is expected_result
        if expected_result:
            assert report.get_result()["diagnostic"] == ""
        else:
            assert report.get_result()["diagnostic"] != ""
