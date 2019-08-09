"""Tests for the input and verification of command-line arguments."""

import pytest

from gator import arguments


VERIFIED = True
NOT_VERIFIED = False


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable."""
    return ["check_commits"]


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


def test_basic_check_correct(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified."""
    gg_arguments = arguments.parse(verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == VERIFIED
