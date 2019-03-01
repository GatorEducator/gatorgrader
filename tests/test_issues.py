"""Test cases for the issues module"""

from gator import issues

TOKEN = 


def test_issue_made():
    """Checks to ensure that issues are correctly being checked"""
    out, num, err = issues.check_issues_made(TOKEN, "GatorEducator/gatorgrader", "gkapfham", 1)
    assert out is True
    assert num == 1
    assert err == 0


def test_issue_comment():
    """Checks to ensure that comments on issues are correctly being checked"""
    out, num, err = issues.check_comments_made(TOKEN, "GatorEducator/gatorgrader", "gkapfham", 1)
    assert out is True
    assert num == 1
    assert err == 0


def test_issue_invalid_token():
    """Checks to ensure that if there is an incorrect token it returns the correct error"""
    _, _, err = issues.check_issues_made("aaa", "GatorEducator/gatorgrader", "gkapfham", 1)
    assert err == -1


def test_issue_invalid_token():
    """Checks to ensure that if there is an incorrect repo it returns the correct error"""
    _, _, err = issues.check_issues_made(TOKEN, "GatorEducator/gator", "gkapfham", 1)
    assert err == -2


def test_comments_invalid_token():
    """Checks to ensure that if there is an incorrect token it returns the correct error"""
    _, _, err = issues.check_comments_made("aaa", "GatorEducator/gatorgrader", "gkapfham", 1)
    assert err == -1


def test_comments_invalid_token():
    """Checks to ensure that if there is an incorrect repo it returns the correct error"""
    _, _, err = issues.check_comments_made(TOKEN, "GatorEducator/gator", "gkapfham", 1)
    assert err == -2
