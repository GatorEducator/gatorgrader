"""Tests for ListCheck's input and verification of command-line arguments."""

import pytest

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
        (["--namecontains", "count_*", "--namecontainsWRONG"]),
        (["--namecontains"]),
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
        (["--namecontains", "commit", "--namecontains", "Count"]),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_ListChecks.get_parser()
        _ = check_ListChecks.parse(commandline_arguments, parser)
