"""Interact with a Git repository."""

import git

from gator import constants
from gator import util


def is_git_repository(repository_path):
    """Return True if repository_path contains a Git repository, False otherwise."""
    # attempt to create a repository using GitPython
    try:
        # it was possible to create the repository, so it must exist
        # this means that the function should return True
        # because it is safe to inspect attributes of this repository
        _ = git.Repo(repository_path).git_dir
        return True
    # it was not possible to create the repository, so it does not exist
    # this means that the function should return False to signal
    # that it is not safe to inspect Git attributes in this non-repo
    except git.exc.InvalidGitRepositoryError:
        return False


def get_commits(repository_path):
    """Return a list of the commits for the repository at the path."""
    # assume that we have not found a Git repository
    # and thus set the default commits lists is []
    commits = constants.versioncontrol.No_Commits
    if is_git_repository(repository_path):
        # the repository_path is a Git repository
        # Try to extract the commits from the repository
        # and return the list of commits if they are available.
        student_repository = git.Repo(repository_path)
        try:
            commits = list(student_repository.iter_commits())
        # In circumstances in which this does not work
        # (e.g., it is a Git repository with no commits)
        # then catch the ValueError, pass, and return the
        # commits as the empty list created previously
        except ValueError:
            pass
    return commits


def count_commits(commits):
    """Return the count of the list of commits."""
    return len(commits)


def commits_greater_than_count(path, expected_count, exact=False):
    """Return count and true if count of commits is greater than limit, else False."""
    # extract the commit log and then count the commits
    commits = get_commits(path)
    number_commits = count_commits(commits)
    # check the condition and also return number_commits
    return util.greater_than_equal_exacted(number_commits, expected_count, exact)
