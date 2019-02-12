from github import Github

# github access
g = Github("username", "password")

# gets the repo
repo = g.get_repo("GatorEducator/gatorgrader")

# prints out the total number of events that have occurred for each state
print("Closed Issues:",repo.get_issues(state="closed").totalCount)
print("Open Issues:",repo.get_issues(state="open").totalCount)
print("Total Issues:",repo.get_issues(state="all").totalCount)

# prints out all events
for issue in repo.get_issues(state="all"):
    print(issue)
