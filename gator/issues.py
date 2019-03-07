"""Get issues from the Github issue tracker and performs checks on them"""

from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException


def check_issues_made(token, repo, name, expected):
    """Returns the number of issues that the given user has made"""
    # github access
    g = Github(token)
    # gets the repo
    try:
        repo = g.get_repo(repo)
    except BadCredentialsException:
        return False, 0, -1
    except UnknownObjectException:
        return False, 0, -2
    issues_made = 0
    for issue in repo.get_issues(state="all"):
        if issue.user.login == name and issue.pull_request is None:
            issues_made += 1
        if issues_made >= expected:
            return True, issues_made, 0
    return issues_made >= expected, issues_made, 0


def check_comments_made(token, repo, name, expected):
    """Returns the number of comments that the given user has made"""
    # github access
    g = Github(token)
    # gets the repo
    try:
        repo = g.get_repo(repo)
    except BadCredentialsException:
        return False, 0, -1
    except UnknownObjectException:
        return False, 0, -2
    comments_made = 0
    for issue in repo.get_issues(state="all"):
        for comment in issue.get_comments():
            if comment.user.login == name and issue.pull_request is None:
                comments_made += 1
            if comments_made >= expected:
                return True, comments_made, 0
    return comments_made >= expected, comments_made, 0
