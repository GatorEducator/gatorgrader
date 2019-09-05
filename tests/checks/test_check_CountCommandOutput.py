"""Tests for CountCommandOutput's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch

from gator import arguments
from gator import report
from gator.checks import check_CountCommandOutput


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_CountCommandOutput.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--commandWRONG", "echo"]),
        (["--command", "run", "--WRONG"]),
        (["--command"]),
        (["--command", "run", "--count", "5", "--WRONG"]),
        (["--command", "run", "--countWRONG", "5"]),
    ],
)
def test_required_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Ensure that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_CountCommandOutput.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--count", "5", "--command", "run_command_first"]),
        (["--count", "5", "--command", "run_command_second"]),
        (["--command", "run_command_first", "--count", "5"]),
        (["--command", "run_command_first", "--count", "5", "--exact"]),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_CountCommandOutput.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--count", "5", "--command", "run_command_first"]),
        (["--count", "5", "--command", "run_command_second"]),
        (["--command", "run_command_first", "--count", "5"]),
        (["--command", "run_command_first", "--count", "5", "--exact"]),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_CountCommandOutput.get_parser()
        _ = check_CountCommandOutput.parse(commandline_arguments, parser)


@pytest.mark.parametrize(
    "commandline_arguments, expected_result",
    [
        (["CountCommandOutput", "--command", "WrongCommand", "--count", "0"], True),
        (
            [
                "CountCommandOutput",
                "--command",
                "WrongCommand",
                "--count",
                "0",
                "--exact",
            ],
            True,
        ),
        (["CountCommandOutput", "--command", "WrongCommand", "--count", "1000"], False),
        (
            [
                "CountCommandOutput",
                "--command",
                "WrongCommand",
                "--count",
                "1000",
                "--exact",
            ],
            False,
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--count",
                "1",
            ],
            True,
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--count",
                "2",
                "--exact",
            ],
            False,
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--count",
                "100",
            ],
            False,
        ),
    ],
)
def test_act_produces_output(commandline_arguments, expected_result, load_checker):
    """Ensure that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check_exists, checker_source, check_file = load_checker(parsed_arguments)
        assert check_exists is True
        check = checker_source.load_plugin(check_file)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is not None
        assert len(check_result) == 1
        assert check_result[0] is expected_result
        # check the contents of the report
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is expected_result
        if expected_result:
            assert report.get_result()["diagnostic"] == ""
        else:
            assert report.get_result()["diagnostic"] != ""
