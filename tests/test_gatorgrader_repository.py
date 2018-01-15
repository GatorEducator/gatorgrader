"""Testing to see if GatorGrader can analyze Git repositories"""

import gatorgrader_repository


def test_gatorgrader_repository_not_zero_commits():
    """Checks to ensure that GatorGrader's repository registers"""
    commits = gatorgrader_repository.get_commmits(".")
    assert len(commits) > 1
    assert len(commits) > 300
