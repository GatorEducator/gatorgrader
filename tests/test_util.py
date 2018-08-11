"""Test cases for the run module"""

from gator import util

VERIFIED = True
NOT_VERIFIED = False


def test_correct_true_readable():
    """Checks to ensure that true input returns yes"""
    human_value = util.get_human_answer(True)
    assert human_value == "Yes"


def test_correct_true_symbol():
    """Checks to ensure that true input returns a heavy checkmark"""
    human_value = util.get_symbol_answer(True)
    assert human_value == "✔"


def test_correct_false_readable():
    """Checks to ensure that false input returns no"""
    human_value = util.get_human_answer(False)
    assert human_value == "No"


def test_correct_false_symbol():
    """Checks to ensure that false input returns heavy x-mark"""
    human_value = util.get_symbol_answer(False)
    assert human_value == "✘"


def test_gatorgrader_home_is_set():
    """Ensure that the gatorgrader_HOME environment variable is set"""
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None


def test_gatorgrader_home_verification_working_verified():
    """Checks that GATORGRADER_HOME verification is working"""
    gatorgrader_home_verified = util.verify_gatorgrader_home("/home/gkapfham/")
    assert gatorgrader_home_verified == VERIFIED


def test_gatorgrader_home_verification_working_notverified():
    """Checks that GATORGRADER_HOME verification is working"""
    gatorgrader_home_verified = util.verify_gatorgrader_home("/home/gkapfham")
    assert gatorgrader_home_verified == NOT_VERIFIED
