"""Store details about the check, its status, and diagnostic information."""

import json
import sys

from gator import constants
from gator import util

# define the name of this module
REPORT = sys.modules[__name__]

# create the empty result table
result = None

# create strings with the name of two report functions
# these are the names of the functions that perform output
# both of these functions exist inside of the report module
# note that these were not moved to constants because they
# are names of functions that exist in this module
TEXT = "output_text"
JSON = "output_json"


def create_result(check, outcome, diagnostic):
    """Create a new result dictionary."""
    result_dictionary = {}
    result_dictionary[constants.results.Check] = check
    result_dictionary[constants.results.Outcome] = outcome
    result_dictionary[constants.results.Diagnostic] = diagnostic
    return result_dictionary


def reset():
    """Reset the global result dictionary."""
    # pylint: disable=global-statement
    global result
    result = None


def set_result(check, outcome, diagnostic):
    """Set the current result dictionary."""
    # pylint: disable=global-statement
    global result
    result = create_result(check, outcome, diagnostic)
    return result


def get_result():
    """Return the result dictionary."""
    # pylint: disable=global-statement
    global result
    return result


def output(dictionary_result, dictionary_format=TEXT):
    """Return the output that the dictionary would produce with the given format."""
    output_function = getattr(REPORT, dictionary_format)
    return output_function(dictionary_result)


def output_text(dictionary_result) -> str:
    """Produce output in textual format."""
    # extract the details and form a string
    check = dictionary_result[constants.results.Check]
    outcome = dictionary_result[constants.results.Outcome]
    diagnostic = dictionary_result[constants.results.Diagnostic]
    # there is a diagnostic, so include it on the next line
    if diagnostic is not constants.markers.Nothing:
        submitted = (
            # display answer with a symbol not a boolean
            util.get_symbol_answer(outcome)
            + constants.markers.Space
            + check
            # SPACE
            + constants.markers.Space
            # NEWLINE
            + constants.markers.Newline
            # TAB
            + constants.markers.Tab
            # ARROW
            + constants.markers.Arrow
            # SPACE
            + constants.markers.Space
            + diagnostic
        )
    # there is no diagnostic, so do not include anything else
    else:
        submitted = util.get_symbol_answer(outcome) + constants.markers.Space + check
    return submitted


def output_json(dictionary_result) -> str:
    """Return output in a JSON-based textual format."""
    return json.dumps(dictionary_result)
