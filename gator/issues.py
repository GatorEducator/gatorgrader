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
    # print(rate.remaining)
    contributors = list()
    if issue.pull_request == None:
        print("Issue:", issue.number)
        # not everyone has a name attached to their github, grabs username if
        # that is the case, if no username grabs email
        try:
            contributors.append(issue.user.name)
        except:
            try:
                contributors.append(issue.user.login)
            except:
                contributors.append(issue.user.email)
        comments = issue.get_comments()
        for comment in comments:
            name = comment.user.login
            # not everyone has a name attached to their github, grabs username if
            # that is the case, if no username grabs email
            # try:
            #     contributors.append(comment.user.name)
            # except:
            #     try:
            #         contributors.append(comment.user.login)
            #     except:
            #         contributors.append(comment.user.email)
            contributors.append(name)
            print(comment.user.login + ":")
            # print(comment.body)
        print(contributors)

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
