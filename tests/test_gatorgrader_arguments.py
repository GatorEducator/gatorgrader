"""Tests for the arguments main program"""

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
    return ["--directories", "D", "F", "G", "--checkfiles", "a", "b", "c"]


@pytest.fixture
def not_verifiable_gg_args():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G", "--checkfiles", "a", "b"]


@pytest.fixture
def not_verifiable_gg_args_missing():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G"]


@pytest.fixture
def not_verifiable_gg_args_missing_comments():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G", "--singlecomments", "2"]


@pytest.fixture
def not_verifiable_gg_args_missing_fragments():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G", "--fragmentcounts", "2", "3", "2"]


@pytest.fixture
def not_verifiable_gg_args_missing_paragraphs():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G", "--paragraphs", "2"]


@pytest.fixture
def not_verifiable_gg_args_missing_sentences():
    """Return arguments that are not verifiable"""
    return ["--directories", "D", "F", "G", "--sentences", "4"]


# pylint: disable=redefined-outer-name
def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct"""
    gg_arguments = arguments.parse(no_gg_args)
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == VERIFIED


def test_arguments_verified(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified"""
    gg_arguments = arguments.parse(verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == VERIFIED


def test_arguments_not_verified(not_verifiable_gg_args):
    """Run arguments with not verifiable arguments and it is not verified"""
    gg_arguments = arguments.parse(not_verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == NOT_VERIFIED


# pylint: disable=bad-continuation
def test_default_argument_values_not_correct_when_missing(
    not_verifiable_gg_args_missing
):
    """The command-line arguments are not correct"""
    gg_arguments = arguments.parse(
        not_verifiable_gg_args_missing
    )
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_comments(
    not_verifiable_gg_args_missing_comments
):
    """The command-line arguments are not correct"""
    gg_arguments = arguments.parse(
        not_verifiable_gg_args_missing_comments
    )
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_fragments(
    not_verifiable_gg_args_missing_fragments
):
    """The command-line arguments are not correct"""
    gg_arguments = arguments.parse(
        not_verifiable_gg_args_missing_fragments
    )
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


def test_default_argument_values_not_correct_when_missing_paragraphs(
    not_verifiable_gg_args_missing_paragraphs
):
    """The command-line arguments are not correct"""
    gg_arguments = arguments.parse(
        not_verifiable_gg_args_missing_paragraphs
    )
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


# pylint: disable=bad-continuation
def test_default_argument_values_not_correct_when_missing_sentences(
    not_verifiable_gg_args_missing_paragraphs
):
    """The command-line arguments are not correct"""
    gg_arguments = arguments.parse(
        not_verifiable_gg_args_missing_paragraphs
    )
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED
