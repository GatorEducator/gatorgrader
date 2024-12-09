"""Test cases for the util module."""

import json
import os
import sys

from unittest.mock import patch

from gator import constants
from gator import files
from gator import util

VERIFIED = True
NOT_VERIFIED = False


def test_correct_true_readable():
    """Check to ensure that true input returns yes."""
    human_value = util.get_human_answer(True)
    assert human_value == "Yes"


def test_correct_true_symbol():
    """Check to ensure that true input returns a heavy checkmark."""
    human_value = util.get_symbol_answer(True)
    assert human_value == "✔"


def test_correct_false_readable():
    """Check to ensure that false input returns no."""
    human_value = util.get_human_answer(False)
    assert human_value == "No"


def test_correct_false_symbol():
    """Check to ensure that false input returns heavy x-mark."""
    human_value = util.get_symbol_answer(False)
    assert human_value == "✘"


def test_gatorgrader_home_is_set():
    """Ensure that the GATORGRADER_HOME environment variable is set."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        gatorgrader_home = util.get_gatorgrader_home()
        # If GATORGRADER_HOME is not set, then it will be set
        # by default to the home directory. These assertions
        # use Pathlib objects to do the comparison so as to
        # ensure that they pass across all operating systems
        current_working_directory = files.create_program_path()
        assert gatorgrader_home is not None
        assert files.create_path(home=gatorgrader_home) == files.create_path(
            home=current_working_directory
        )


def test_gatorgrader_home_is_set_after_os_dictionary_set(tmpdir):
    """Ensure that the GATORGRADER_HOME environment variable is set."""
    tmpdir.mkdir("gatorgrader")
    os.environ["GATORGRADER_HOME"] = str(tmpdir) + "/" + "gatorgrader/"
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None
    assert "gatorgrader" in gatorgrader_home


def test_gatorgrader_home_is_set_after_os_dictionary_set_no_trailing(tmpdir):
    """Ensure that the GATORGRADER_HOME environment variable is set."""
    tmpdir.mkdir("gatorgrader")
    os.environ["GATORGRADER_HOME"] = str(tmpdir) + "/" + "gatorgrader"
    gatorgrader_home = util.get_gatorgrader_home()
    assert gatorgrader_home is not None
    assert "gatorgrader" in gatorgrader_home


# def test_gatorgrader_home_is_set_after_os_dictionary_set_wrong_directory(tmpdir):
#     """Ensure that the GATORGRADER_HOME environment variable is set."""
#     os.environ["GATORGRADER_HOME"] = str(tmpdir) + "/" + "INCORRECT"
#     gatorgrader_home = util.get_gatorgrader_home()
#     assert gatorgrader_home is not None
#     assert "gatorgrader" in gatorgrader_home


def test_gatorgrader_home_verification_working_not_verified_none_given():
    """Check that GATORGRADER_HOME verification is working."""
    gatorgrader_home_verified = util.verify_gatorgrader_home(None)
    assert gatorgrader_home_verified is NOT_VERIFIED


def test_gatorgrader_home_verification_working_not_verified_blank_given():
    """Check that GATORGRADER_HOME verification is working."""
    gatorgrader_home_verified = util.verify_gatorgrader_home("")
    assert gatorgrader_home_verified is NOT_VERIFIED


def test_gatorgrader_home_verification_working_verified(tmp_path):
    """Check that GATORGRADER_HOME verification is working."""
    # this must be a valid directory on the filesystem
    home_directory = tmp_path / "gatorgrader"
    home_directory.mkdir()
    gatorgrader_home_verified = util.verify_gatorgrader_home(str(home_directory))
    assert gatorgrader_home_verified is VERIFIED


def test_gatorgrader_home_verification_working_notverified_wrong(tmp_path):
    """Check that GATORGRADER_HOME verification is working."""
    # the real directory does not end in "gatorgrader" and thus it is not valid
    home_directory = tmp_path / "gatorgraderNOT"
    home_directory.mkdir()
    gatorgrader_home_verified = util.verify_gatorgrader_home(str(home_directory))
    assert gatorgrader_home_verified is NOT_VERIFIED


def test_gatorgrader_home_verification_working_notverified_internal(tmp_path):
    """Check that GATORGRADER_HOME verification is working."""
    # this directory does not end in "gatorgrader" and thus it is not valid
    # in this test, though, the gatorgrader directory does exist in the path
    home_directory = tmp_path / "gatorgrader"
    home_directory.mkdir()
    home_directory = home_directory / "finaldirectorywrong"
    home_directory.mkdir()
    gatorgrader_home_verified = util.verify_gatorgrader_home(str(home_directory))
    assert gatorgrader_home_verified is NOT_VERIFIED


def test_json_detection_found():
    """Check if a valid JSON string is detected as JSON."""
    dictionary = {"a": "b"}
    json_string = json.dumps(dictionary)
    is_valid_json = util.is_json(json_string)
    assert is_valid_json is True


def test_json_detection_not_found():
    """Check if a not valid JSON string is not detected as JSON."""
    not_dictionary = "Command\nNot\nFound\n"
    is_valid_json = util.is_json(not_dictionary)
    assert is_valid_json is False


def test_flatten_dictionary():
    """Check to see if the dictionary is flattened correctly."""
    input_dictionary = {
        "leave.py": {1: 4},
        "run.py": {1: 8},
        "entities.py": {1: 18},
        "files.py": {1: 33},
        "display.py": {1: 0},
        "util.py": {1: 26},
        "markdown.py": {1: 6},
        "__init__.py": {1: 0},
        "arguments.py": {1: 107},
        "comments.py": {1: 6},
        "orchestrate.py": {1: 38},
        "constants.py": {1: 28},
        "report.py": {1: 19},
        "invoke.py": {1: 89},
        "fragments.py": {1: 68},
        "repository.py": {1: 18},
    }
    flat_input_dictionary = util.flatten_dictionary_values(input_dictionary)
    assert flat_input_dictionary["leave.py"] == 4
    assert flat_input_dictionary["run.py"] == 8


def test_relational_operator_exacted_true_not_exacted():
    """Check to see if the exacted relational operator returns True, no exacting."""
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10)
    assert relation_boolean is True
    assert relation_value == 100
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10, False)
    assert relation_boolean is True
    assert relation_value == 100


def test_relational_operator_exacted_true_exacted():
    """Check to see if the exacted relational operator returns True."""
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 100, True)
    assert relation_boolean is True
    assert relation_value == 100


def test_relational_operator_exacted_false_not_exacted():
    """Check to see if the exacted relational operator returns False, no exacting."""
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100)
    assert relation_boolean is False
    assert relation_value == 10
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100, False)
    assert relation_boolean is False
    assert relation_value == 10


def test_relational_operator_exacted_false_exacted():
    """Check to see if the exacted relational operator returns False."""
    relation_boolean, relation_value = util.greater_than_equal_exacted(10, 100, True)
    assert relation_boolean is False
    assert relation_value == 10
    relation_boolean, relation_value = util.greater_than_equal_exacted(100, 10, True)
    assert relation_boolean is False
    assert relation_value == 100


def test_number_to_words_ordinal_and_cardinal():
    """Check to see if numbers can be converted to ordinal or cardinal words."""
    # note that ordinal is the default
    number_as_word = util.get_number_as_words(42)
    assert number_as_word == "forty-second"
    # it is also possible to request cardinal words
    number_as_word = util.get_number_as_words(42, constants.words.Cardinal)
    assert number_as_word == "forty-two"


def test_find_in_empty_dictionary_min():
    """Check if the None value is found in an empty dictionary."""
    input = {}
    found_values = util.get_first_minimum_value(input)
    assert found_values[0] == 0
    assert found_values[1] == 0


def test_find_in_empty_dictionary_max():
    """Check if the None value is found in an empty dictionary."""
    input = {}
    found_values = util.get_first_maximum_value(input)
    assert found_values[0] == 0
    assert found_values[1] == 0


def test_find_maximum_in_dictionary_single_max():
    """Check if the maximum value is found in a dictionary."""
    input = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    found_values = util.get_first_maximum_value(input)
    assert found_values[0] == "Mike"
    assert found_values[1] == 52


def test_find_maximum_in_dictionary_multiple_max():
    """Check if the maximum value is found in a dictionary."""
    input = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43, "Robert": 52}
    found_values = util.get_first_maximum_value(input)
    assert found_values[0] == "Mike"
    assert found_values[1] == 52


def test_find_minimum_in_dictionary_single_min():
    """Check if the minimum value is found in a dictionary."""
    input = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    found_values = util.get_first_minimum_value(input)
    assert found_values[0] == "Sarah"
    assert found_values[1] == 12


def test_find_minimum_in_dictionary_multiple_min():
    """Check if the minimum value is found in a dictionary."""
    input = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43, "Gina": 12}
    found_values = util.get_first_minimum_value(input)
    assert found_values[0] == "Sarah"
    assert found_values[1] == 12


def test_word_diagnostic_single_min_first():
    """Check to see if diagnostic is produced with a single minimum value."""
    word_count_dictionary_file_one = {1: 4, 2: 5, 3: 10}
    word_count_dictionary = {"file_one": word_count_dictionary_file_one}
    word_diagnostic = util.get_word_diagnostic(word_count_dictionary)
    assert word_diagnostic[0] == "in the first"


def test_word_diagnostic_single_min_last():
    """Check to see if diagnostic is produced with a single minimum value."""
    word_count_dictionary_file_one = {1: 10, 2: 5, 3: 4}
    word_count_dictionary = {"file_one": word_count_dictionary_file_one}
    word_diagnostic = util.get_word_diagnostic(word_count_dictionary)
    assert word_diagnostic[0] == "in the third"


def test_word_diagnostic_empty_dictionary():
    """Check to see if diagnostic is produced with an empty dictionary."""
    word_count_dictionary = {}
    word_diagnostic = util.get_word_diagnostic(word_count_dictionary)
    assert word_diagnostic == ("", "")


def test_sum_dictionary_values():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_two = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_three = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 1}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    sum_dictionary = util.sum_dictionary_values(outer_dictionary)
    assert sum_dictionary["input_file_one"] == (21 + 52 + 12 + 43)
    assert sum_dictionary["input_file_two"] == (21 + 52 + 12 + 43)
    assert sum_dictionary["input_file_three"] == (21 + 52 + 12 + 1)


def test_find_minimum_in_dictionary_single_max_deep():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_two = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_three = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 1}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_first_maximum_value_deep(outer_dictionary)
    assert found[0] == "input_file_one"
    assert found[1] == ("Mike", 52)


def test_find_not_equal_value_deep_all_not_same():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_two = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    input_file_three = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 1}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_first_not_equal_value_deep(outer_dictionary, 43)
    assert found[0] == "input_file_one"
    assert found[1] == ("John", 21)


def test_find_not_equal_value_not_deep_all_not_same():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 52, "Sarah": 12, "Bob": 43}
    found = util.get_first_not_equal_value(input_file_one, 43)
    assert found[0] == "John"
    assert found[1] == 21


def test_find_not_equal_value_deep_all_same():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_two = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_three = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_first_not_equal_value_deep(outer_dictionary, 21)
    assert found == {}


def test_get_file_diagnostic_deep_exact_empty_dictionary():
    """Check if getting a file diagnostic with an empty dictionary works."""
    empty_dictionary = {}
    value = 10
    found = util.get_file_diagnostic_deep_exact(empty_dictionary, value)
    assert found == ("in a file", 0)


def test_get_file_diagnostic_deep_exact_deep_dictionary_not_equal():
    """Check if getting a file diagnostic with a non-deep dictionary works."""
    input_file_one = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_two = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_three = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 22}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_file_diagnostic_deep_exact(outer_dictionary, 21)
    assert found


def test_get_file_diagnostic_deep_exact_deep_dictionary_all_equal():
    """Check if getting a file diagnostic with a non-deep dictionary works."""
    input_file_one = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_two = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    input_file_three = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_file_diagnostic_deep_exact(outer_dictionary, 21)
    assert found == ("in a file", 0)


def test_get_file_diagnostic_deep_not_exact_empty_dictionary():
    """Check if getting a file diagnostic with an empty dictionary works."""
    empty_dictionary = {}
    found = util.get_file_diagnostic_deep_not_exact(empty_dictionary)
    assert found == ("in a file", 0)


def test_get_file_diagnostic_deep_empty_dictionary():
    """Check if getting a file diagnostic with an empty dictionary works."""
    empty_dictionary = {}
    # this is a wrapper function for get_file_diagnostic_deep_not_exact
    found = util.get_file_diagnostic_deep(empty_dictionary)
    assert found == ("in a file", 0)


def test_find_not_equal_value_not_deep():
    """Check if the maximum value is found in a dictionary deep."""
    input_file_one = {"John": 21, "Mike": 21, "Sarah": 21, "Bob": 21}
    found = util.get_first_not_equal_value(input_file_one, 21)
    assert found == (0, 0)


def test_find_minimum_in_dictionary_single_max_deep_words():
    """Check if the minimum value is found in a dictionary deep."""
    input_file_one = {1: 10, 2: 5, 3: 4}
    input_file_two = {1: 10, 2: 5, 3: 4}
    input_file_three = {1: 10, 2: 5, 3: 1}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    found = util.get_first_minimum_value_deep(outer_dictionary)
    assert found[0] == "input_file_three"
    assert found[1] == (3, 1)


def test_find_minimum_in_dictionary_single_max_deep_words_diagnostic():
    """Check to see if diagnostic is produced with a single minimum value."""
    input_file_one = {1: 10, 2: 5, 3: 4}
    input_file_two = {1: 10, 2: 5, 3: 4}
    input_file_three = {1: 10, 2: 5, 3: 1}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    diagnostic = util.get_word_diagnostic(outer_dictionary)
    assert diagnostic is not None
    assert diagnostic[0] == "in the third"
    assert diagnostic[1] == "input_file_three"


def test_find_minimum_in_dictionary_single_max_deep_words_diagnostic_all_same():
    """Check to see if diagnostic is produced with a single minimum value."""
    input_file_one = {1: 10, 2: 10, 3: 10}
    input_file_two = {1: 10, 2: 10, 3: 10}
    input_file_three = {1: 10, 2: 10, 3: 10}
    outer_dictionary = {
        "input_file_one": input_file_one,
        "input_file_two": input_file_two,
        "input_file_three": input_file_three,
    }
    diagnostic = util.get_word_diagnostic(outer_dictionary, 10)
    assert diagnostic is not None
    assert diagnostic[0] == ""
    assert diagnostic[1] == ""


def test_find_minimum_in_dictionary_single_max_deep_words_diagnostic_realistic():
    """Check to see if diagnostic is produced with a single minimum value."""
    outer_dictionary = {
        "README.md": {
            1: 3,
            2: 12,
            3: 82,
            4: 2,
            5: 152,
            6: 51,
            7: 68,
            8: 66,
            9: 104,
            10: 1,
            11: 53,
            12: 102,
            13: 59,
            14: 47,
            15: 98,
            16: 123,
            17: 34,
            18: 42,
            19: 108,
            20: 8,
            21: 11,
        },
        "LICENSE.md": {
            1: 29,
            2: 17,
            3: 98,
            4: 77,
            5: 45,
            6: 55,
            7: 35,
            8: 49,
            9: 112,
            10: 64,
            11: 11,
            12: 12,
            13: 16,
            14: 25,
            15: 50,
            16: 15,
            17: 58,
            18: 36,
            19: 90,
            20: 27,
            21: 41,
            22: 118,
            23: 124,
            24: 19,
            25: 14,
            26: 76,
            27: 113,
            28: 22,
            29: 41,
            30: 70,
            31: 76,
            32: 25,
            33: 39,
            34: 101,
            35: 38,
            36: 30,
            37: 136,
            38: 67,
            39: 109,
            40: 76,
            41: 46,
            42: 85,
            43: 69,
            44: 34,
            45: 96,
            46: 42,
            47: 26,
            48: 47,
            49: 58,
            50: 60,
            51: 50,
            52: 88,
            53: 41,
            54: 96,
            55: 77,
            56: 34,
            57: 83,
            58: 36,
            59: 63,
            60: 148,
            61: 73,
            62: 163,
            63: 30,
            64: 110,
            65: 84,
            66: 44,
            67: 83,
            68: 40,
            69: 33,
            70: 88,
            71: 105,
            72: 61,
            73: 41,
            74: 51,
            75: 13,
            76: 21,
            77: 36,
            78: 46,
            79: 65,
        },
    }
    util.get_word_diagnostic(outer_dictionary)
