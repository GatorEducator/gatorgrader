"""Tests for ListCheck's input and verification of command-line arguments."""

import os
import pytest
import sys

from unittest.mock import patch

from gator import arguments
from gator import report
from gator.checks import check_ListChecks


def test_no_arguments_correct_system_exit(not_raises):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with not_raises(SystemExit):
        parser = check_ListChecks.get_parser()
        _ = check_ListChecks.parse([], parser)


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
def test_optional_commandline_arguments_cannot_verify(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_ListChecks.parse(commandline_arguments)
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
        (["--namecontains", "check_"]),
        (["--namecontains", "commit", "--namecontains", "Count"]),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_ListChecks.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--namecontains", "check_"]),
        (["--namecontains", "commit"]),
        (["--namecontains", "Count"]),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_ListChecks.get_parser()
        _ = check_ListChecks.parse(commandline_arguments, parser)


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
