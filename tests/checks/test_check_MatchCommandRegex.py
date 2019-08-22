"""Tests for MatchCommandRegex's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch

from gator import arguments
from gator import checkers
from gator import report
from gator.checks import check_MatchCommandRegex


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_MatchCommandRegex.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 3


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--countWRONG", "5"]),
        (["--count", "5", "--regexWRONG", "hi"]),
        (["--count", "5", "--regexWRONG", "hi", "--exact"]),
        (["--count", "5", "--regexWRONG"]),
        (["--exact"]),
    ],
)
def test_optional_commandline_arguments_cannot_verify(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_MatchCommandRegex.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 3


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--command", "run_command_first", "--regex", "regex", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "regex*", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "regex+", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "(regex)+", "--count", "5"]),
        (["--command", "run_command_second", "--regex", "regex", "--count", "5"]),
        (
            [
                "--command",
                "run_command_first",
                "--regex",
                "regex",
                "--count",
                "5",
                "--exact",
            ]
        ),
        (
            [
                "--command",
                "run_command_second",
                "--regex",
                "regex",
                "--count",
                "5",
                "--exact",
            ]
        ),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_MatchCommandRegex.get_parser()
        _ = check_MatchCommandRegex.parse(commandline_arguments, parser)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--command", "run_command_first", "--regex", "regex", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "regex*", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "regex+", "--count", "5"]),
        (["--command", "run_command_first", "--regex", "(regex)+", "--count", "5"]),
        (["--command", "run_command_second", "--regex", "regex", "--count", "5"]),
        (
            [
                "--command",
                "run_command_first",
                "--regex",
                "regex",
                "--count",
                "5",
                "--exact",
            ]
        ),
        (
            [
                "--command",
                "run_command_second",
                "--regex",
                "regex",
                "--count",
                "5",
                "--exact",
            ]
        ),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_MatchCommandRegex.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments, expected_result",
    [
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "Noregex",
                "--count",
                "0",
            ],
            True,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "(regex)*",
                "--count",
                "1",
            ],
            True,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "(regex)+",
                "--count",
                "1",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "Noregex",
                "--count",
                "0",
                "--exact",
            ],
            True,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "Noregex",
                "--count",
                "1000",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                "WrongCommand",
                "--regex",
                "Noregex",
                "--count",
                "1000",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "Corr",
                "--count",
                "1",
            ],
            True,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "Corr",
                "--count",
                "2",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "Corr",
                "--count",
                "100",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "Corr",
                "--count",
                "100",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "(Corr)*",
                "--count",
                "100",
                "--exact",
            ],
            False,
        ),
        (
            [
                "MatchCommandRegex",
                "--command",
                'echo "CorrectCommand"',
                "--regex",
                "(Corr)+",
                "--count",
                "100",
                "--exact",
            ],
            False,
        ),
    ],
)
def test_act_produces_output(commandline_arguments, expected_result):
    """Ensure that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        external_checker_directory = checkers.get_checker_dir(parsed_arguments)
        checker_source = checkers.get_source([external_checker_directory])
        check_name = checkers.get_chosen_check(parsed_arguments)
        check_file = checkers.transform_check(check_name)
        check_exists = checkers.verify_check_existence(check_file, checker_source)
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
