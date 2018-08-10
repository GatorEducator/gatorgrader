"""Stores details about a check, its status, and diagnostic information"""

details = {}
result_count = 0

CHECK = "check"
OUTCOME = "outcome"
DIAGNOSTIC = "diagnostic"


def create_result(check, outcome, diagnostic):
    """Create a new result"""
    result_dictionary = {}
    result_dictionary[CHECK] = check
    result_dictionary[OUTCOME] = outcome
    result_dictionary[DIAGNOSTIC] = diagnostic
    return result_dictionary


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
