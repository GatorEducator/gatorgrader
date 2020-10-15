"""integration testing to ensure grading consistency"""

import requests
from subprocess import run
import os
from shutil import rmtree


GITHUB_API_URI = "https://api.github.com/orgs/GatorEducator/repos"
# temp dir for the clone repos
REPOS_DIR = "repos"
# starting directory (just in case something interrupts, we can still clean up)
ORIGINAL_DIR = ""


def fetch_repos():
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


def grade_repo(repo):
    """clones and grades a repository; returns True if it passes, False if it fails"""
    proc1 = subprocess.run(["git clone", repo[1]], check=True)
    os.chdir(repo[0])
    proc2 = subprocess.run(["gradle grade"])
    return True if proc2.returncode == 0 else False


# should fail
def grade_starter(repo):
    if not grade_repo(repo):
        return None
    else:
        raise Exception(f"{repo[0]} passed when it should have failed.")


# should pass
def grade_solution(repo):
    if grade_repo(repo):
        return None
    else:
        raise Exception(f"{repo[0]} failed when it should have passed.")


def cleanup():
    global REPOS_DIR
    if os.path.exists(REPOS_DIR):
        shutil.rmtree(REPOS_DIR)


def setup():
    global ORIGINAL_DIR, REPOS_DIR
    ORIGINAL_DIR = os.getcwd()
    os.mkdir(REPOS_DIR)
    os.chdir(REPOS_DIR)


def ensure():
    try:
        repos = fetch_repos()
        for starter in repos["starters"]:
            grade_starter(starter)
        for solution in repos["solutions"]:
            grade_solution(solution)
    except Exception as e:
        print(e)
    finally:
        cleanup()

# FIXME: how do they want me to handle exceptions on the upper level?
# FIXME: integrate into CI
# FIXME: test with gradle (I don't have it on my workstation yet)
# FIXME: windows/mac support
