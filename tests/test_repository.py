"""Test cases for the repository module."""

import sys

from gator import repository


def test_repository_not_zero_commits():
    """Check to ensure that GatorGrader's repository registers."""
    commits = repository.get_commmits(".")
    assert len(commits) > 1


def test_repository_not_zero_commits_extra_method():
    """Check to ensure that GatorGrader's repository registers."""
    commits = repository.get_commmits(".")
    assert repository.count_commits(commits) > 1


def test_repository_not_zero_commits_greater_than():
    """Check to ensure that commit counts work correctly."""
    valid, __ = repository.commits_greater_than_count(".", 1)
    assert valid is True


def test_repository_not_zero_commits_greater_than_exacted():
    """Check to ensure that commit counts work correctly."""
    valid, __ = repository.commits_greater_than_count(".", 1, True)
    assert valid is False


def test_repository_commits_not_huge():
    """Check to ensure that commit counts work correctly."""
    valid, __ = repository.commits_greater_than_count(".", sys.maxsize)
    assert valid is False


def test_repository_commits_not_huge_exacted():
    """Check to ensure that commit counts work correctly."""
    valid, __ = repository.commits_greater_than_count(".", sys.maxsize, True)
    assert valid is False
