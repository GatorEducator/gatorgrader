"""Functions that interact with a Git repository"""

from git import Repo


MASTER = "master"


def get_commmits(path):
    """Returns a list of the commits for the repo at path"""
    repository = Repo(path)
    commits = list(repository.iter_commits(MASTER))
    return commits


def count_commits(commits):
    """Returns the count of the list of commits"""
    return len(commits)
