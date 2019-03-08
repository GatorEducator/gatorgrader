"""Stores details about the check, its status, and diagnostic information"""

import json
import sys

from gator import util

REPORT = sys.modules[__name__]

result = None

CHECK = "check"
OUTCOME = "outcome"
DIAGNOSTIC = "diagnostic"

TEXT = "output_text"
JSON = "output_json"

ARROW = "➔"
EMPTY_STRING = ""
NEWLINE = "\n"
SPACE = " "
TAB = "   "


def create_result(check, outcome, diagnostic):
    """Create a new result dictionary"""
    result_dictionary = {}
    result_dictionary[CHECK] = check
    result_dictionary[OUTCOME] = outcome
    result_dictionary[DIAGNOSTIC] = diagnostic
    return result_dictionary


def reset():
    """Reset the global result dictionary"""
    # pylint: disable=global-statement
    global result
    result = None


def set_result(check, outcome, diagnostic):
    """Set the current result dictionary"""
    # pylint: disable=global-statement
    global result
    result = create_result(check, outcome, diagnostic)
    return result


def get_result():
    """Return the result dictionary"""
    # pylint: disable=global-statement
    global result
    return result


def output(dictionary_result, dictionary_format=TEXT):
    """Return the output that the dictionary would produce with the given format"""
    output_function = getattr(REPORT, dictionary_format)
    return output_function(dictionary_result)


def output_text(dictionary_result) -> str:
    """Produce output in textual format"""
    # extract the details and form a string
    check = dictionary_result[CHECK]
    outcome = dictionary_result[OUTCOME]
    diagnostic = dictionary_result[DIAGNOSTIC]
    # there is a diagnostic, so include it on the next line
    if diagnostic is not EMPTY_STRING:
        submitted = (
            util.get_symbol_answer(outcome)
            + SPACE
            + check
            + SPACE
            + NEWLINE
            + TAB
            + ARROW
            + SPACE
            + diagnostic
        )
    # there is no diagnostic, so do not include anything else
    else:
        submitted = util.get_symbol_answer(outcome) + SPACE + check
    return submitted


def output_json(dictionary_result) -> str:
    """Return output in a JSON-based textual format"""
    return json.dumps(result)
