"""Tests for MatchCommandFragment's input and verification of command-line arguments."""

import pytest

from gator import arguments
from gator import checkers
from gator import report
from gator.checks import check_MatchCommandFragment


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_MatchCommandFragment.parse([])
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
        (["--count", "5", "--fragmentWRONG", "hi"]),
        (["--count", "5", "--fragmentWRONG", "hi", "--exact"]),
        (["--count", "5", "--exactWRONG"]),
        (["--exact"]),
    ],
)
def test_optional_commandline_arguments_cannot_verify(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_MatchCommandFragment.parse(commandline_arguments)
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
        (["--command", "run_command_first", "--fragment", "fragment", "--count", "5"]),
        (["--command", "run_command_second", "--fragment", "fragment", "--count", "5"]),
        (["--command", "run_command_first", "--fragment", "fragment", "--count", "5", "--exact"]),
        (["--command", "run_command_second", "--fragment", "fragment", "--count", "5", "--exact"]),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_MatchCommandFragment.get_parser()
        _ = check_MatchCommandFragment.parse(commandline_arguments, parser)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--command", "run_command_first", "--fragment", "fragment", "--count", "5"]),
        (["--command", "run_command_second", "--fragment", "fragment", "--count", "5"]),
        (["--command", "run_command_first", "--fragment", "fragment", "--count", "5", "--exact"]),
        (["--command", "run_command_second", "--fragment", "fragment", "--count", "5", "--exact"]),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Ensure that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_MatchCommandFragment.parse(commandline_arguments)
