"""Tests for CountCommits' input and verification of command-line arguments."""

import pytest

from gator.checks import check_CountCommits


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_CountCommits.parse([])
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
    [(["--countWRONG", "5"]), (["--count", "5", "--exactWRONG"]), (["--exact"])],
)
def test_optional_commandline_arguments_cannot_verify(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_CountCommits.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


@pytest.mark.parametrize(
    "commandline_arguments", [(["--count", "5"]), (["--count", "5", "--exact"])]
)
def test_optional_commandline_arguments_can_verify(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_CountCommits.parse(commandline_arguments)
