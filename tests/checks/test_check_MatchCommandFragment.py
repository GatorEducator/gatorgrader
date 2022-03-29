"""Tests for MatchCommandFragment's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch

from gator import arguments
from gator import report
from gator.exceptions import InvalidCheckArgumentsError
from gator.checks import check_MatchCommandFragment


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        ([]),
        (["--countWRONG", "5"]),
        (["--count", "5", "--fragmentWRONG", "hi"]),
        (["--count", "5", "--fragmentWRONG", "hi", "--exact"]),
        (["--count", "5", "--exactWRONG"]),
        (["--exact"]),
    ],
)
def test_optional_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(InvalidCheckArgumentsError) as excinfo:
        _ = check_MatchCommandFragment.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output or error
    assert captured.err == ""
    assert captured.out == ""
    assert excinfo.value.check_name == "MatchCommandFragment"
    assert excinfo.value.usage
    assert excinfo.value.message


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--command", "run_command_first", "--fragment", "fragment", "--count", "5"]),
        (["--command", "run_command_second", "--fragment", "fragment", "--count", "5"]),
        (
            [
                "--command",
                "run_command_first",
                "--fragment",
                "fragment",
                "--count",
                "5",
                "--exact",
            ]
        ),
        (
            [
                "--command",
                "run_command_second",
                "--fragment",
                "fragment",
                "--count",
                "5",
                "--exact",
            ]
        ),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(InvalidCheckArgumentsError):
        _ = check_MatchCommandFragment.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments, expected_result",
    [
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
            ],
            True,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
                "--exact",
            ],
            True,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "1000",
            ],
            False,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "1000",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "1",
            ],
            True,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "2",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "100",
            ],
            False,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "100",
                "--exact",
            ],
            False,
        ),
    ],
)
def test_act_produces_output(commandline_arguments, expected_result, load_check):
    """Ensure that using the check produces output."""
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
