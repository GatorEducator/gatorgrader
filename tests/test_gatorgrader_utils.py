""" test cases for the gatorgrader_utils module """

import gatorgrader_util


def test_correct_true_readable():
    """Checks to ensure that true input returns yes"""
    human_value = gatorgrader_util.get_human_answer(True)
    assert human_value == "Yes"


def test_correct_false_readable():
    """Checks to ensure that false input returns no"""
    human_value = gatorgrader_util.get_human_answer(False)
    assert human_value == "No"
