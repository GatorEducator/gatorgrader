"""Stores details about a check, its status, and diagnostic information"""

import json

from gator import util

details = {}
result_count = 0

FIRST = 0

CHECK = "check"
OUTCOME = "outcome"
DIAGNOSTIC = "diagnostic"

REPORT = "report"
TEXT = "output_text"
JSON = "output_json"

NEWLINE = "\n"
SPACE = " "
EMPTY_STRING = ""


def create_result(check, outcome, diagnostic):
    """Create a new result"""
    result_dictionary = {}
    result_dictionary[CHECK] = check
    result_dictionary[OUTCOME] = outcome
    result_dictionary[DIAGNOSTIC] = diagnostic
    return result_dictionary


def reset():
    """Reset the details dictionary and the count"""
    # pylint: disable=global-statement
    global details
    global result_count
    details = {}
    result_count = 0


def add_result(check, outcome, diagnostic):
    """Add a new result to the details dictionary"""
    # pylint: disable=global-statement
    global result_count
    global details
    new_result = create_result(check, outcome, diagnostic)
    details[result_count] = new_result
    new_result_count = result_count
    result_count = result_count + 1
    return new_result_count, new_result


def get_details():
    """Return the details dictionary"""
    return details


def get_detail(index):
    """Return a result from the details dictionary"""
    return details[index]


def get_size():
    """Return the size of the details dictionary"""
    return len(details)


def contains_nested_dictionary(dictionary):
    """Determines if the provided dictionary contains another dictionary"""
    if dictionary:
        for item in list(dictionary.values()):
            if isinstance(item, dict):
                return True
    return False


def output(dictionary_result, dictionary_format=TEXT):
    """Return the output that the dictionary would produce"""
    output_function = getattr(REPORT, dictionary_format)
    output_list = []
    output_function(dictionary_result, output_list)


def form_single_output_line(check, outcome, diagnostic):
    """Produce a single line of output in a textual format"""
    # there is a diagnostic, so include it on the next line
    if diagnostic is not EMPTY_STRING:
        submitted = (
            check + SPACE + util.get_symbol_answer(outcome) + NEWLINE + diagnostic
        )
    # there is no diagnostic, so do not include anything else
    else:
        submitted = (
            check + SPACE + util.get_symbol_answer(outcome)
        )
    return submitted


def output_text(dictionary_result, output_list):
    """Produce output in a textual format"""
    # the dictionary is not nested, so extract the details and form a string
    if not contains_nested_dictionary(dictionary_result):
        check = dictionary_result[CHECK]
        outcome = dictionary_result[OUTCOME]
        diagnostic = dictionary_result[DIAGNOSTIC]
        # put the string into the output list
        submitted = form_single_output_line(check, outcome, diagnostic)
        output_list.append(submitted)
    # dictionary is nested, so iterate through dictionaries recursively
    else:
        for nested_dictionary in dictionary_result.values():
            output_text(nested_dictionary, output_list)
