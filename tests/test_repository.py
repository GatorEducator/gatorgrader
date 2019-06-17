"""Test cases for the repository module."""

import sys

from git import Repo

from gator import repository


def test_repository_not_zero_commits():
    """Check to ensure that GatorGrader's repository registers."""
    commits = repository.get_commits(".")
    assert len(commits) > 1


def test_repository_not_zero_commits_extra_method():
    """Check to ensure that GatorGrader's repository registers."""
    commits = repository.get_commits(".")
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


def test_detect_not_git_repository(tmpdir):
    """Ensure that it is possible to detect that a directory is not a Git repository."""
    # by default, the tmpdir is not a Git repository
    # the check for the existence of a repository should be False
    detected_git_repository = repository.is_git_repository(str(tmpdir))
    assert detected_git_repository is False


def test_detect_git_repository(tmpdir):
    """Ensure that it is possible to detect that a directory is not a Git repository."""
    # create a Git repository using GitPython
    _ = Repo.init(str(tmpdir))
    # since the repository was created in the tmpdir
    # the check for the existence of a repository should be True
    detected_git_repository = repository.is_git_repository(str(tmpdir))
    assert detected_git_repository is True


def test_no_commits_in_new_git_repository(tmpdir):
    """Ensure that it is possible to detect that a directory is not a Git repository."""
    # create a Git repository using GitPython
    _ = Repo.init(str(tmpdir))
    # since the repository was created in the tmpdir
    # the check for the existence of a repository should be True
    detected_git_repository = repository.is_git_repository(str(tmpdir))
    assert detected_git_repository is True
    commits = repository.get_commits(str(tmpdir))
    assert len(commits) == 0


def test_nocrash_when_not_repository(tmpdir):
    """Ensure that a get_commits not in a repository does not crash."""
    # since there is, by default, no repository in tmpdir
    # then a call to get_commits will will return an empty list
    commits = repository.get_commits(str(tmpdir))
    assert len(commits) == 0
