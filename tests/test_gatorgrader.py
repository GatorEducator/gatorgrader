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
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G', '--checkfiles', 'a', 'b']


@pytest.fixture
def not_verifiable_gg_args_missing():
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G']


@pytest.fixture
def not_verifiable_gg_args_missing_comments():
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G', '--singlecomments', '2']


@pytest.fixture
def not_verifiable_gg_args_missing_fragments():
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G', '--fragmentcounts', '2', '3', '2']


@pytest.fixture
def not_verifiable_gg_args_missing_paragraphs():
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G', '--paragraphs', '2']


@pytest.fixture
def not_verifiable_gg_args_missing_sentences():
    """Return arguments that are not verifiable"""
    return ['--directories', 'D', 'F', 'G', '--sentences', '4']


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


def test_default_argument_values_not_correct_when_missing(
        not_verifiable_gg_args_missing):
    """The default command-line arguments are not correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args_missing)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_comments(
        not_verifiable_gg_args_missing_comments):
    """The default command-line arguments are not correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args_missing_comments)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_fragments(
        not_verifiable_gg_args_missing_fragments):
    """The default command-line arguments are not correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args_missing_fragments)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_paragraphs(
        not_verifiable_gg_args_missing_paragraphs):
    """The default command-line arguments are not correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args_missing_paragraphs)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_sentences(
        not_verifiable_gg_args_missing_paragraphs):
    """The default command-line arguments are not correct"""
    gg_arguments = gatorgrader.parse_gatorgrader_arguments(
        not_verifiable_gg_args_missing_paragraphs)
    gatorgrader_args_verified = gatorgrader.verify_gatorgrader_arguments(
        gg_arguments)
    assert gatorgrader_args_verified == NOT_VERIFIED


def test_gatorgrader_home_is_set():
    """Ensure that the gatorgrader_HOME environment variable is set"""
    gatorgrader_home = gatorgrader.get_gatorgrader_home()
    assert gatorgrader_home is not None


def test_gatorgrader_home_verification_working_verified():
    """Checks that GATORGRADER_HOME verification is working"""
    gatorgrader_home_verified = gatorgrader.verify_gatorgrader_home(
        "/home/gkapfham/")
    assert gatorgrader_home_verified == VERIFIED


def test_gatorgrader_home_verification_working_notverified():
    """Checks that GATORGRADER_HOME verification is working"""
    gatorgrader_home_verified = gatorgrader.verify_gatorgrader_home(
        "/home/gkapfham")
    assert gatorgrader_home_verified == NOT_VERIFIED
