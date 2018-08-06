"""Tests for the input and checking of command-line arguments"""

import pytest

from gator import arguments

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
