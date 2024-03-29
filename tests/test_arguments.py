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
    assert counted_newlines >= 2


def test_no_arguments_incorrect_system_exit_not_verified(capsys):
    """Ensure that no command-line arguments causes SystemExit crash and is not verified."""
    with pytest.raises(SystemExit):
        gg_arguments, remaining_arguments = arguments.parse([])
        arguments_args_verified = arguments.verify(gg_arguments)
        assert arguments_args_verified == NOT_VERIFIED
    # capture the output so that test output is not polluted
    _ = capsys.readouterr()


def test_basic_check_correct():
    """Ensure when given verifiable arguments, there is no error and it is verified."""
    gg_arguments, remaining_arguments = arguments.parse(["CheckCommits"])
    args_verified = arguments.verify(gg_arguments)
    assert args_verified == VERIFIED


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "CheckCommits"]),
        (["--json", "--nowelcome", "CheckCommits"]),
        (["--nowelcome", "CheckCommits"]),
        (["--checkerdir", "./gator/checks", "CheckCommits"]),
        (["--description", "Are there 12 commits?", "CheckCommits"]),
        (
            [
                "--checkerdir",
                "./gator/checks",
                "--description",
                "Are there 18 commits?",
                "CheckCommits",
            ]
        ),
        (
            [
                "--json",
                "--nowelcome",
                "--checkerdir",
                "./gator/checks",
                "--description",
                "Are there 18 commits?",
                "CheckCommits",
            ]
        ),
    ],
)
def test_optional_commandline_arguments_can_verify(commandline_arguments):
    """Check that correct optional command-line arguments check correctly."""
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True


def test_checkerdir_is_valid_arguments_verify(tmpdir):
    """Check that command-line argument with valid directory verifies."""
    _ = tmpdir.mkdir("checks").join("check_FakeMessages.py")
    assert len(tmpdir.listdir()) == 1
    # this directory exists on the file system and verification should work
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, "check_FakeMessages"]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True


def test_checkerdir_is_not_valid_arguments_verify(tmpdir):
    """Check that command-line argument with valid directory verifies."""
    _ = tmpdir.mkdir("checks").join("check_FakeMessages.py")
    assert len(tmpdir.listdir()) == 1
    # this directory does not exist on the file system and verification should not work
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checksWRONG"
    commandline_arguments = ["--checkerdir", checker_directory, "check_FakeMessages"]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is False


def test_description_is_valid_arguments_verify():
    """Check that command-line argument with valid string verifies."""
    commandline_arguments = [
        "--description",
        "Do you have fake things?",
        "check_FakeMessages",
    ]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True


def test_description_not_specified_is_not_valid_arguments_verify(capsys):
    """Check that command-line argument without valid string verifies."""
    commandline_arguments = ["--description", "--json", "check_FakeMessages"]
    with pytest.raises(SystemExit):
        gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        _ = arguments.verify(gg_arguments)
    captured = capsys.readouterr()
    assert "--description: expected one argument" in captured.err


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--description", "", "CheckCommits"]),
        (["--description", 'Run the "check" check', "CheckCommits"]),
    ],
)
def test_description_is_not_valid_arguments_verify(commandline_arguments):
    """Check that command-line argument without valid string verifies."""
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is False


def test_help_produces_output(capsys):
    """Ensure that when given a request for help, it is produced correctly."""
    with pytest.raises(SystemExit):
        _ = arguments.parse(["--help"])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines > 0
    # standard error has lines produced by specialized print_help
    assert "required argument:" in captured.out
    assert "usage:" in captured.out
    assert "all checks:" in captured.out
    assert "internal checks:" in captured.out
