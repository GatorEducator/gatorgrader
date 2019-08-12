"""Tests for the input and verification of command-line arguments."""

import pytest

from gator import arguments


VERIFIED = True
NOT_VERIFIED = False


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = arguments.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


def test_no_arguments_incorrect_system_exit_not_verified(capsys):
    """No command-line arguments causes SystemExit crash and is not verified."""
    with pytest.raises(SystemExit):
        gg_arguments = arguments.parse([])
        arguments_args_verified = arguments.verify(gg_arguments)
        assert arguments_args_verified == NOT_VERIFIED
    # capture the output so that test output is not polluted
    _ = capsys.readouterr()


def test_basic_check_correct():
    """When given verifiable arguments, there is no error and it is verified."""
    gg_arguments = arguments.parse(["check_commits"])
    args_verified = arguments.verify(gg_arguments)
    assert args_verified == VERIFIED


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "check_commits"]),
        (["--json", "--nowelcome", "check_commits"]),
        (["--nowelcome", "check_commits"]),
    ],
)
def test_optional_commandline_arguments_can_verify(commandline_arguments):
    """Check that correct optional command-line arguments check correctly."""
    gg_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--jsonFF", "check_commits"]),
        (["--json", "--nowelcomeFF", "check_commits"]),
        (["--nowelcomeFF", "check_commits"]),
        (["--checkerdir", "checker_directory"]),
        (["--checkerdirFF", "checker_directory", "check_commits"]),
    ],
)
def test_optional_commandline_arguments_cannot_verify(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = arguments.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


def test_checkerdir_is_valid_arguments_verify(tmpdir):
    """Check that command-line argument with valid directory verifies."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    # this directory exists on the file system and verification should work
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, "check_messages"]
    gg_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True


def test_checkerdir_is_not_valid_arguments_verify(tmpdir):
    """Check that command-line argument with valid directory verifies."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    # this directory does not exist on the file system and verification should not work
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checksWRONG"
    commandline_arguments = ["--checkerdir", checker_directory, "check_messages"]
    gg_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is False
