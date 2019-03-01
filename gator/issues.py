# """Get issues from the Github issue tracker and performs checks on them"""
from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException
# from github.GithubException import BadCredentialsException
# from git import Repo

def check_issues_made(token, repo, name):
    """Returns the number of issues that the given user has made"""
    # github access
    g = Github(token)
    # gets the repo
    try:
        repo = g.get_repo(repo)
    except BadCredentialsException:
        return -1
    except UnknownObjectException:
        return -2
    issues_made = 0
    for issue in repo.get_issues(state="all"):
        if issue.user.login == name and issue.pull_request == None:
            issues_made += 1
    return issues_made

def check_comments_made(token, repo, name):
    """Returns the number of comments that the given user has made"""
    # github access
    g = Github(token)
    # gets the repo
    try:
        repo = g.get_repo(repo)
    except BadCredentialsException:
        return -1
    except UnknownObjectException:
        return -2
    comments_made = 0
    for issue in repo.get_issues(state="all"):
        for comment in issue.get_comments():
            if issue.pull_request == None and comment.user.login == name:
                comments_made += 1
    return comments_made
