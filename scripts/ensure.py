import json
import requests

def fetch_repos():
    response = requests.get("https://api.github.com/orgs/GatorEducator/repos", headers={"Accept": "application/vnd.github.v3+json"})
    repos = response.json()
    # ("REPOSITORY_NAME", "CLONE_URL")
    repodata = [(repo["name"], repo["clone_url"]) for repo in repos]
    return repodata

