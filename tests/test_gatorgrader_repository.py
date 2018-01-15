"""Testing to see if GatorGrader can analyze Git repositories"""

import gatorgrader_repository


def test_gatorgrader_repository_not_zero_commits():
    """Checks to ensure that GatorGrader's repository registers"""
    commits = gatorgrader_repository.get_commmits(".")
    assert len(commits) > 1


def test_gatorgrader_repository_not_zero_commits_extra_method():
    """Checks to ensure that GatorGrader's repository registers"""
    commits = gatorgrader_repository.get_commmits(".")
    assert gatorgrader_repository.count_commits(commits) > 1


def test_gatorgrader_repository_not_zero_commits_greater_than():
    """Checks to ensure that GatorGrader's repository registers"""
    assert gatorgrader_repository.commits_greater_than_count(".", 1) is True
