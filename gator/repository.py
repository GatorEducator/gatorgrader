"""Interact with a Git repository"""

from git import Repo
from gator import util


MASTER = "master"


def get_commmits(path):
    """Returns a list of the commits for the repo at path"""
    student_repository = Repo(path)
    # pass in None so that the default (the current branch) is used
    # this avoids problems with being checked out in different branches
    # alternatively, we could detect the current HEAD and use that
    commits = list(student_repository.iter_commits())
    return commits


def count_commits(commits):
    """Returns the count of the list of commits"""
    return len(commits)


def commits_greater_than_count(path, expected_count, exact=False):
    """Returns count and true if count of commits is greater than limit, else False"""
    # extract the commit log and then count the commits
    commits = get_commmits(path)
    number_commits = count_commits(commits)
    # check the condition and also return number_commits
    return util.greater_than_equal_exacted(number_commits, expected_count, exact)

def check_non_alphanumerics():
    """ Returns if emoji were entered in commit"""
    commits = get_commmits(path)
    if (
        commits.isalnum()
    ):
        return True
    else:
        return False
