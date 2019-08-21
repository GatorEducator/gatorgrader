"""Utility functions."""

from gator import constants
from gator import files

import json
import os
import sys

from num2words import num2words


def verify_gatorgrader_home(current_gatorgrader_home):
    """Verify that the GATORGRADER_HOME variable is set correctly."""
    # assume that the home is not verified and try to prove otherwise
    # a directory is verified if:
    # 1) it exists on the file system
    # 2) is ends in the word "gatorgrader"
    verified_gatorgrader_home = False
    # pylint: disable=bad-continuation
    if current_gatorgrader_home is not None:
        # the provided input parameter is not empty, so try to
        # create a path for the directory contained in parameter
        possible_gatorgrader_home = files.create_path(home=current_gatorgrader_home)
        # this directory exists and the final part of the directory is "gatorgrader"
        if (
            possible_gatorgrader_home.exists()
            and possible_gatorgrader_home.name == constants.paths.Home
        ):
            verified_gatorgrader_home = True
    return verified_gatorgrader_home


def get_gatorgrader_home():
    """Return GATORGRADER_HOME environment variable if is valid directory."""
    current_gatorgrader_home = os.environ.get(constants.environmentvariables.Home)
    # the current_gatorgrader_home is acceptable, so use it
    if verify_gatorgrader_home(current_gatorgrader_home) is not False:
        print("GATORGRADER_HOME was set by environment variable")
        gatorgrader_home = current_gatorgrader_home
    # the current GATORGRADER_HOME is not valid, so create the
    # home for this program to be the current working directory
    else:
        print("GATORGRADER_HOME was not set by environment variable")
        gatorgrader_home = str(files.create_cwd_path())
    print("gatorgrader_home")
    print(gatorgrader_home)
    print(os.path.dirname(os.path.realpath(sys.argv[0])))
    return gatorgrader_home


def get_human_answer(boolean_value):
    """Return a human readable response for the boolean_value."""
    if boolean_value is True:
        return "Yes"
    return "No"


def get_symbol_answer(boolean_value):
    """Return a symbol response for the boolean_value."""
    if boolean_value is True:
        return "✔"
    return "✘"


def flatten_dictionary_values(input_dictionary):
    """Flatten by extracting the value from the dictionary that is a value."""
    flat_dictionary = {}
    for filename, file_count_dictionary in input_dictionary.items():
        # the internal dictionary will have a single key,value pair
        # extract the value and then store it in the flat_dictionary
        key = next(iter(file_count_dictionary))
        extracted_value = file_count_dictionary[key]
        flat_dictionary[filename] = extracted_value
    return flat_dictionary


def get_first_value_deep(input_dictionary, finder=min):
    """Return all deep values matched by a finder function."""
    filename_count_dictionary = {}
    for filename, paragraph_count_dictionary in input_dictionary.items():
        filename_minimum = get_first_value(paragraph_count_dictionary, finder)
        filename_count_dictionary[filename] = filename_minimum
    outer_found_value = get_first_value(filename_count_dictionary, finder)
    return outer_found_value


def get_first_value(input_dictionary, finder=min):
    """Return the values matched by a finder function."""
    # pick the key and value that is matched by the finder
    # note that the return is in the format (key, value)
    # the dictionary is empty, so return 0 for the key and value
    if not input_dictionary:
        return (0, 0)
    # the dictionary is not empty, so return the located (key, value)
    return finder(
        input_dictionary.items(), key=lambda input_dictionary: input_dictionary[1]
    )


def get_first_maximum_value(input_dictionary):
    """Return the first maximum value."""
    return get_first_value(input_dictionary, max)


def get_first_minimum_value(input_dictionary):
    """Return the first minimum value."""
    return get_first_value(input_dictionary, min)


def get_first_maximum_value_deep(input_dictionary):
    """Return the first maximum value deep."""
    return get_first_value_deep(input_dictionary, max)


def get_first_minimum_value_deep(input_dictionary):
    """Return the first minimum value deep."""
    return get_first_value_deep(input_dictionary, min)


def is_json(potential_json):
    """Determine if a string is in JSON format."""
    try:
        json.loads(potential_json)
    except ValueError:
        return False
    return True


def greater_than_equal_exacted(first, second, exact=False):
    """Return True if first >= second unless exact, then True if ==, otherwise False."""
    if not exact and first >= second:
        return True, first
    if exact and first == second:
        return True, first
    return False, first


def get_number_as_words(number, format=constants.words.Ordinal):
    """Return a textual version of the provided word."""
    return num2words(number, to=format)


def get_word_diagnostic(word_count_dictionary):
    """Create a full diagnostic based on the dictionary of (paragraph, word counts)."""
    # create a diagnostics like "in the third paragraph" based on the dictionary
    # that contains the words counts in each of the paragraphs of a document
    if word_count_dictionary:
        paragraph_number_details_list = get_first_minimum_value_deep(
            word_count_dictionary
        )
        filename_for_paragraph_number_details = paragraph_number_details_list[0]
        paragraph_number_details = paragraph_number_details_list[1]
        paragraph_number = paragraph_number_details[0]
        paragraph_number_as_word = get_number_as_words(paragraph_number)
        paragraph_number_as_word_phrase = (
            constants.words.In_The + constants.markers.Space + paragraph_number_as_word
        )
        return paragraph_number_as_word_phrase, filename_for_paragraph_number_details
    # since there are no paragraphs and no counts of words because the dictionary
    # is empty, return the empty string instead of a diagnostic phrase
    # for both the paragraph number as word phrase and the filename
    return constants.markers.Nothing, constants.markers.Nothing


def get_file_diagnostic(file_count_dictionary):
    """Create a full diagnostic based on the dictionary of (file name, entity counts)."""
    # create a diagnostics like "in the <filename>" based on the dictionary
    # that contains the fragment counts in each of the files with a wildcard
    if file_count_dictionary:
        file_details = get_first_minimum_value(file_count_dictionary)
        file_name = file_details[0]
        file_name_phrase = constants.words.In_The + constants.markers.Space + file_name
        return file_name_phrase
    # since there are no file names and no counts of entities because the dictionary
    # is empty, return the "in a file" string instead of a diagnostic phrase
    return constants.markers.In_A_File
