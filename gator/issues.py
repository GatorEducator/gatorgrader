"""Get issues from the Github issue tracker and performs checks on them"""
from github import Github
# from git import Repo

# github access
g = Github("username","password")

# gets the repo
repo = g.get_repo("Repo")

def check_issues_made(name):
    """Returns the number of issues that the given user has made"""
    issues_made = 0
    for issue in repo.get_issues(state="all"):
        if issue.user.login == name and issue.pull_request == None:
            issues_made += 1
    return issues_made

def check_comments_made(name):
    """Returns the number of comments that the given user has made"""
    comments_made = 0
    for issue in repo.get_issues(state="all"):
        for comment in issue.get_comments():
            if comment.user.login == name and issue.pull_request == None:
                comments_made += 1
    return comments_made

print(check_issues("username"))
print(check_comments("username"))

# issue = repo.get_issue(85)
# contributors = set()
# contributors.add(issue.user.name)
# if issue.pull_request == None:
#     comments = issue.get_comments()
#     for comment in comments:
#         contributors.add(comment.user.name)
#         print(comment.user.name, ":")
#         print(comment.body)
# print(contributors)
