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


def test_grader_reports_missing_repository(tmp_path, monkeypatch):
    """Check that gator.grader returns a failed result for a missing repository."""
    monkeypatch.chdir(tmp_path)
    description, passed, diagnostic = gator.grader(
        ["CountCommits", "--count", "1"],
    )
    assert "commit(s)" in description
    assert passed is False
    assert "Did not find a Git repository at" in diagnostic
