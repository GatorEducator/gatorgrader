"""Functions that interact with a Git repository"""

from git import Repo


MASTER = "master"


def get_commmits(path):
    """Returns a list of the commits for the repo at path"""
    repository = Repo(path)
    # pass in None so that the default (the current branch) is used
    # this avoids problems with being checked out in different branches
    # alternatively, we could detect the current HEAD and use that
    commits = list(repository.iter_commits())
    return commits


def count_commits(commits):
    """Returns the count of the list of commits"""
    return len(commits)


def commits_greater_than_count(path, expected_count):
    """Returns true if count of commits is greater than limit, else False"""
    commits = get_commmits(path)
    number_commits = count_commits(commits)
    if number_commits >= expected_count:
        return True
    return False
