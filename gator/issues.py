# """Get issues from the Github issue tracker and performs checks on them"""
from github import Github
#
# # github access
# g = Github("username", "password")
#
# # gets the repo
# repo = g.get_repo("GatorEducator/gatorgrader")
#
# # prints out the total number of events that have occurred for each state
# # print("Closed Issues:", repo.get_issues(state="closed").totalCount)
# # print("Open Issues:", repo.get_issues(state="open").totalCount)
# # print("Total Issues:", repo.get_issues(state="all").totalCount)
#
# # prints out all events
# for issue in repo.get_issues(state="all"):
#     # print(rate.remaining)
#     contributors = list()
#     if issue.pull_request == None:
#         print("Issue:", issue.number)
#         # not everyone has a name attached to their github, grabs username if
#         # that is the case, if no username grabs email
#         try:
#             contributors.append(issue.user.name)
#         except:
#             try:
#                 contributors.append(issue.user.login)
#             except:
#                 contributors.append(issue.user.email)
#         comments = issue.get_comments()
#         for comment in comments:
#             name = comment.user.login
#             # not everyone has a name attached to their github, grabs username if
#             # that is the case, if no username grabs email
#             # try:
#             #     contributors.append(comment.user.name)
#             # except:
#             #     try:
#             #         contributors.append(comment.user.login)
#             #     except:
#             #         contributors.append(comment.user.email)
#             contributors.append(name)
#             print(comment.user.login + ":")
#             # print(comment.body)
#         print(contributors)
#
# # issue = repo.get_issue(85)
# # contributors = set()
# # contributors.add(issue.user.name)
# # if issue.pull_request == None:
# #     comments = issue.get_comments()
# #     for comment in comments:
# #         contributors.add(comment.user.name)
# #         print(comment.user.name, ":")
# #         print(comment.body)
# # print(contributors)

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
get_specific_issue()
