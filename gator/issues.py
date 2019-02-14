"""Get issues from the Github issue tracker and performs checks on them"""
from github import Github

# github access
g = Github("ZachAndrews98", "ZachAndr2020@!")

# gets the repo
repo = g.get_repo("GatorEducator/gatorgrader")

# prints out the total number of events that have occurred for each state
# print("Closed Issues:", repo.get_issues(state="closed").totalCount)
# print("Open Issues:", repo.get_issues(state="open").totalCount)
# print("Total Issues:", repo.get_issues(state="all").totalCount)

# prints out all events
for issue in repo.get_issues(state="all"):
    if issue.pull_request == None:
        comments = issue.get_comments()
        for comment in comments:
            print(comment.user, ":")
            print(comment.body)
