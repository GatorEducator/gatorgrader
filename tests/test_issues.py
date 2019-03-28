"""Test cases for the issues module"""

from gator import issues

# will need to not use this and take out the second half of the token later.
TOKEN = "3e20125561f10fa4df42"


def test_issue_made_pass():
    """Checks to ensure that issues are correctly being checked"""
    out, num, err = issues.check_issues_made(
        TOKEN + "ac38d5bdd114df9a0ee8",
        "GatorEducator/test-repository",
        "yeej2",
        1,
        "all",
    )
    assert out is True
    assert num == 1
    assert err == 0


def test_issues_made_fail():
    """Checks when issues_made is less than expected"""
    out, num, err = issues.check_issues_made(
        TOKEN + "ac38d5bdd114df9a0ee8",
        "GatorEducator/test-repository",
        "yeej2",
        2,
        "all",
    )
    assert out is False
    assert num == 1
    assert err == 0


def test_issue_comment_pass():
    """Checks to ensure that comments on issues are correctly being checked"""
    out, num, err = issues.check_comments_made(
        TOKEN + "ac38d5bdd114df9a0ee8",
        "GatorEducator/test-repository",
        "yeej2",
        1,
        "all",
    )
    assert out is True
    assert num == 1
    assert err == 0


def test_issue_comment_fail():
    """Checks to ensure that comments on issues are correctly being checked"""
    out, num, err = issues.check_comments_made(
        TOKEN + "ac38d5bdd114df9a0ee8",
        "GatorEducator/test-repository",
        "yeej2",
        2,
        "all",
    )
    assert out is False
    assert num == 1
    assert err == 0


def test_issue_invalid_token():
    """Checks to ensure that an incorrect token returns the correct error"""
    __, __, err = issues.check_issues_made(
        "aaa", "GatorEducator/test-repository", "yeej2", 1, "all"
    )
    assert err == -1


# pylint: disable=function-redefined
def test_issue_invalid_repo():
    """Checks to ensure that if there is an incorrect repo it returns the correct error"""
    __, __, err = issues.check_issues_made(
        TOKEN + "ac38d5bdd114df9a0ee8", "GatorEducator/gator", "yeej2", 1, "all"
    )
    assert err == -2


# def test_check_issues_made():
#     """Checks the final output of check_issues_made"""
#     actual_output = issues.check_issues_made(
#         TOKEN + "ac38d5bdd114df9a0ee8", "GatorEducator/test-repository", "yeej2", 1, "all"
#     )
#     expected_output =


# pylint: disable=function-redefined
def test_comments_invalid_token():
    """Checks to ensure that if there is an incorrect token it returns the correct error"""
    __, __, err = issues.check_comments_made(
        "aaa", "GatorEducator/test-repository", "yeej2", 1, "all"
    )
    assert err == -1


def test_comments_invalid_repo():
    """Checks to ensure that if there is an incorrect repo it returns the correct error"""
    __, __, err = issues.check_comments_made(
        TOKEN + "ac38d5bdd114df9a0ee8", "GatorEducator/gator", "yeej2", 1, "all"
    )
    assert err == -2
