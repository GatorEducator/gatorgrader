"""integration testing to ensure grading consistency

To activate this script, ensure() must be called.

* __setup() begins by creating a temporary folder in which the repositories will be tested.
* __fetch_repos() then fetches names and urls of repositories to test, separating the starters and the solutions.
* __grade_starter() and __grade_solution() both interface __grade_repo(), which uses `gradle` to grade each repository (True if pass, False if fail).
* Both __grade_starter() and __grade_solution() raise an exception if the output is unexpected.
* Ultimately, __cleanup() removes the temporary directory and all of its contents, leaving no trace of the testing.
"""


import requests
from subprocess import run
import os
from shutil import rmtree


GITHUB_API_URI = "https://api.github.com/orgs/GatorEducator/repos"
# temp dir for the clone repos
REPOS_DIR = "repos"
# starting directory (just in case something interrupts, we can still clean up)
ORIGINAL_DIR = ""


def __fetch_repos():
    """fetches starter/solution repositories from GatorEducator; returns two tuple arrays"""
    global GITHUB_API_URI
    response = requests.get(GITHUB_API_URI, headers={"Accept": "application/vnd.github.v3+json"})
    repos = response.json()
    repodata = {"starters": [], "solutions": []}
    for repo in repos:
        if "assignment-start" in repo["name"]:
            repodata["starters"].append((repo["name"], repo["clone_url"]))
        elif "assignment-solution" in repo["name"]:
            repodata["solutions"].append((repo["name"], repo["clone_url"]))
    return repodata


def __grade_repo(repo):
    """clones and grades a repository; returns True if it passes, False if it fails"""
    proc1 = run(["git", "clone", repo[1]], check=True)
    os.chdir(repo[0])
    proc2 = run(["gradle", "grade"])
    os.chdir(REPOS_DIR)
    return True if proc2.returncode == 0 else False


# should fail
def __grade_starter(repo):
    """wrapper for starter repository, see __grade_repo()"""
    if not __grade_repo(repo):
        return None # good
    else:
        raise Exception(f"{repo[0]} passed when it should have failed.")


# should pass
def __grade_solution(repo):
    """wrapper for solution repository, see __grade_repo()"""
    if __grade_repo(repo):
        return None # good
    else:
        raise Exception(f"{repo[0]} failed when it should have passed.")


def __cleanup():
    """removes temporary directory used in testing"""
    global REPOS_DIR
    if os.path.exists(REPOS_DIR):
        rmtree(REPOS_DIR)


def __setup():
    """gets current working directory and sets up temporary directory used in testing"""
    global ORIGINAL_DIR, REPOS_DIR
    ORIGINAL_DIR = os.getcwd()
    if not os.path.exists(REPOS_DIR):
        os.mkdir(REPOS_DIR)
    os.chdir(REPOS_DIR)
    # get absolute path
    REPOS_DIR = os.getcwd()


def ensure():
    """module wrapper; initiates testing"""
    try:
        __setup()
        repos = __fetch_repos()
        for starter in repos["starters"]:
            __grade_starter(starter)
        for solution in repos["solutions"]:
            __grade_solution(solution)
    except Exception as e:
        print(e)
    finally:
        __cleanup()


# FIXME: how do they want me to handle exceptions on the upper level?
# FIXME: integrate into CI
# FIXME: windows/mac support
# FIXME: async
