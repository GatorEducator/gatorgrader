"""Stores details about a check, its status, and diagnostic information"""

import json

details = {}
result_count = 0

FIRST = 0

CHECK = "check"
OUTCOME = "outcome"
DIAGNOSTIC = "diagnostic"

REPORT = "report"
TEXT = "output_text"
JSON = "output_json"


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
    output_function(dictionary_result)


def output_text(dictionary_result):
    """Produce output in a textual format"""
