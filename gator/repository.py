"""Interact with a Git repository."""

import git

from gator import constants, util


def is_git_repository(repository_path):
    """Return True if repository_path contains a Git repository, False otherwise."""
    try:
        # GitPython verifies the repository while constructing it,
        # so a successfully-created repository is safe to inspect
        _ = git.Repo(repository_path).git_dir
        return True
    # GitPython raises these exceptions when the path is missing, not a
    # repository, or otherwise unusable; they all mean that the path
    # cannot be treated as a Git repository
    except (
        git.exc.NoSuchPathError,
        git.exc.InvalidGitRepositoryError,
        git.exc.GitCommandNotFound,
        git.exc.GitCommandError,
        OSError,
    ):
        return False


def get_commits(repository_path):
    """Return a list of the commits for the repository at the path."""
    # a repository that cannot be inspected has no commits to report
    commits = constants.versioncontrol.No_Commits
    if is_git_repository(repository_path):
        student_repository = git.Repo(repository_path)
        try:
            commits = list(student_repository.iter_commits())
        # GitPython raises a ValueError for a valid repository that has
        # no commits, so keep the empty list instead of failing the check
        except ValueError:
            pass
    return commits


def count_commits(commits):
    """Return the count of the list of commits."""
    return len(commits)


def commits_greater_than_count(path, expected_count, exact=False):
    """Return count and True if count of commits is greater than limit, else False."""
    # extract the commit log and then count the commits
    commits = get_commits(path)
    number_commits = count_commits(commits)
    # check the condition and also return number_commits
    return util.greater_than_equal_exacted(
        number_commits, expected_count, exact
    )
