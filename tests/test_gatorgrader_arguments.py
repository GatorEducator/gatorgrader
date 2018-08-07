"""Tests for the input and checking of command-line arguments"""

import pytest

from gator import arguments

EMPTY_STRING = ""
ERROR = "error:"

VERIFIED = True
NOT_VERIFIED = False


@pytest.fixture
def no_gg_args():
    """Return no command-line arguments"""
    return []


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable"""
    return ["--directory", "D", "--file", "a"]


# pylint: disable=redefined-outer-name
def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct"""
    gg_arguments = arguments.parse(no_gg_args)
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


# pylint: disable=redefined-outer-name
def test_arguments_verified(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified"""
    gg_arguments = arguments.parse(verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == VERIFIED


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--directoryy", "D"]),
        (["--directory", "D", "F"]),
        (["--filles", "F"]),
        (["--file", "m", "f"]),
        (["-file", "f"]),
        (["-directory", "f"]),
    ],
)
def test_module_argument_not_verifiable_syserror(chosen_arguments, capsys):
    """Check that not valid arguments will not verify correctly"""
    with pytest.raises(SystemExit):
        arguments.parse(chosen_arguments)
    standard_out, standard_err = capsys.readouterr()
    assert standard_out is EMPTY_STRING
    assert ERROR in standard_err


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "F"]),
        (["--file", "F"]),
    ],
)
def test_invalid_argument_combinations_not_accepted(chosen_arguments):
    """Check that not invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "F"]),
        (["--file", "F"]),
    ],
)
def test_is_valid_file_not_valid(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file(parsed_arguments)
    assert verified_arguments is False
