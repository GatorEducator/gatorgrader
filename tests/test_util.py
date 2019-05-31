"""Test cases for the util module"""

import json
import os

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
    """Ensure that the GATORGRADER_HOME environment variable is set"""
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None


def test_gatorgrader_home_is_set_after_os_dictionary_set():
    """Ensure that the GATORGRADER_HOME environment variable is set"""
    os.environ["GATORGRADER_HOME"] = "/home/gkapfham/working/source/gatorgrader/"
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None
    assert "gatorgrader" in gatorgrader_home


def test_gatorgrader_home_is_set_after_os_dictionary_set_no_trailing():
    """Ensure that the gatorgrader_HOME environment variable is set"""
    os.environ["GATORGRADER_HOME"] = "/home/gkapfham/working/source/gatorgrader"
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None
    assert "gatorgrader" in gatorgrader_home


def test_gatorgrader_home_verification_working_verified(tmp_path):
    """Checks that GATORGRADER_HOME verification is working"""
    home_directory = tmp_path / "gatorgrader"
    home_directory.mkdir()
    gatorgrader_home_verified = util.verify_gatorgrader_home(str(home_directory))
    assert gatorgrader_home_verified == VERIFIED


def test_gatorgrader_home_verification_working_notverified():
    """Checks that GATORGRADER_HOME verification is working"""
    gatorgrader_home_verified = util.verify_gatorgrader_home("/home/gkapfham")
    assert gatorgrader_home_verified == NOT_VERIFIED


def test_json_detection_found():
    """Check if a valid JSON string is detected as JSON"""
    dictionary = {"a": "b"}
    json_string = json.dumps(dictionary)
    is_valid_json = util.is_json(json_string)
    assert is_valid_json is True


def test_json_detection_not_found():
    """Check if a not valid JSON string is not detected as JSON"""
    not_dictionary = "Command\nNot\nFound\n"
    is_valid_json = util.is_json(not_dictionary)
    assert is_valid_json is False


def test_relational_operator_exacted_true_not_exacted():
    """Checks to see if the exacted relational operator returns True, no exacting"""
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10)
    assert relation_boolean is True
    assert relation_value == 100
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10, False)
    assert relation_boolean is True
    assert relation_value == 100


def test_relational_operator_exacted_true_exacted():
    """Checks to see if the exacted relational operator returns True"""
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 100, True)
    assert relation_boolean is True
    assert relation_value == 100


def test_relational_operator_exacted_false_not_exacted():
    """Checks to see if the exacted relational operator returns False, no exacting"""
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100)
    assert relation_boolean is False
    assert relation_value == 10
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100, False)
    assert relation_boolean is False
    assert relation_value == 10


def test_relational_operator_exacted_false_exacted():
    """Checks to see if the exacted relational operator returns False"""
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100, True)
    assert relation_boolean is False
    assert relation_value == 10
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10, True)
    assert relation_boolean is False
    assert relation_value == 100
