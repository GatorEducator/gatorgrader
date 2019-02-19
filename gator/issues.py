# """Get issues from the Github issue tracker and performs checks on them"""
from github import Github
# from git import Repo

def check_issues_made(token, repo, name):
    """Returns the number of issues that the given user has made"""
    # github access
    g = Github(token)
    # gets the repo
    repo = g.get_repo(repo)
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
    repo = g.get_repo(repo)
    comments_made = 0
    for issue in repo.get_issues(state="all"):
        for comment in issue.get_comments():
            if comment.user.login == name and issue.pull_request == None:
                comments_made += 1
        else:
            return 0
    return comments_made

def get_specific_issue():
    """Get issues from the Github issue tracker and performs checks on them"""
    i=1
    # github access
    g = Github("23c5f97ad16447382d64dca0184bf66146535841")

    # gets the repo
    repo = g.get_repo("GatorEducator/gatorgrader")

    #Used for testing specific issues user inputs

    #option = input("Choose your issue, otherwise type 'continue' : ")
    #if option == "continue":

        # prints out the total number of events that have occurred for each state
    print("Closed Issues:", repo.get_issues(state="closed").totalCount)
    print("Open Issues:", repo.get_issues(state="open").totalCount)
    print("Total Issues:", repo.get_issues(state="all").totalCount)

        # prints out all events
    for issue in repo.get_issues(state="all"):
        if issue.pull_request == None:
            print("Issue #", issue.number)
            print(issue.title + ": ")
            print(issue.body, "\n")
            print(repo.get_issue(number = i))
            i+=1
    exit()


    #Used for testing specific issues uer inputs
    # else:
    #         #print out specific issue and throw error for non-integers
    #         try:
    #             print(repo.get_issue(number=int(option)))
    #
    #         except:
    #             print("You've entered an invalid entry.")

#calls get_specific_issue function
# get_specific_issue()
