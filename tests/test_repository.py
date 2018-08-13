"""Test cases for the repository module"""

import sys

from gator import repository


def test_repository_not_zero_commits():
    """Checks to ensure that GatorGrader's repository registers"""
    commits = repository.get_commmits(".")
    assert len(commits) > 1


def test_repository_not_zero_commits_extra_method():
    """Checks to ensure that GatorGrader's repository registers"""
    commits = repository.get_commmits(".")
    assert repository.count_commits(commits) > 1


def test_repository_not_zero_commits_greater_than():
    """Checks to ensure that GatorGrader's repository registers"""
    valid, __ = repository.commits_greater_than_count(".", 1)
    assert valid is True


def test_repository_commits_not_huge():
    """Checks to ensure that GatorGrader's repository registers"""
    valid, __ = repository.commits_greater_than_count(".", 1)
    assert valid is True
