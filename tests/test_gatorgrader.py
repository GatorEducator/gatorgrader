"""Tests for the gatorgrader module"""

import pytest

import gatorgrader

VERIFIED = True
NOT_VERIFIED = False


@pytest.fixture
def no_gg_args():
    """Return no command-line arguments"""
    return []


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable"""
    return ['--directories', 'D', 'F', 'G', '--checkfiles', 'a', 'b', 'c']


@pytest.fixture
def not_verifiable_gg_args():
    """Return arguments that are verifiable"""
    return ['--directories', 'D', 'F', 'G', '--checkfiles', 'a', 'b']


def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(no_gg_args)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == VERIFIED


def test_gatorgrader_verified(verifiable_gg_args):
    """Run gatorgrader with verifiable arguments and it is verified"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(verifiable_gg_args)
    gg_args_verified = gatorgrader.verify_gatorgrader_arguments(gg_arguments)
    assert gg_args_verified == VERIFIED


def test_gatorgrader_not_verified(not_verifiable_gg_args):
    """Run gatorgrader with not verifiable arguments and it is not verified"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args)
    gg_args_verified = gatorgrader.verify_gatorgrader_arguments(gg_arguments)
    assert gg_args_verified == NOT_VERIFIED
