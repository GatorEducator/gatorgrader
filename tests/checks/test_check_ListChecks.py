"""Tests for ListCheck's input and verification of command-line arguments."""

import pytest

from pluginbase import PluginBase

from gator import arguments
from gator import checkers
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


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "ListChecks"]),
        (["--json", "--nowelcome", "ListChecks"]),
        (["--nowelcome", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks"]),
    ],
)
def test_act_produces_output(commandline_arguments):
    """Check that using the check produces output."""
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
    assert check_result is not None
    assert len(check_result) > 1
