"""Test cases for the gator module."""

import pytest

import gator


def test_grader_can_be_called():
    """Check if gator.grader() can be called."""
    description, passed, diagnostic = gator.grader(
        [
            "MatchCommandFragment",
            "--command",
            "WrongCommand",
            "--fragment",
            "NoFragment",
            "--count",
            "0",
        ],
    )
    assert "command" in description
    assert passed is True
    assert diagnostic == ""


def test_grader_fails_with_exception():
    """Check if gator.grader() fails with an exception."""
    with pytest.raises(gator.InvalidSystemArgumentsError):
        gator.grader(
            [
                "--json",
                "NotACheck",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
            ],
        )
