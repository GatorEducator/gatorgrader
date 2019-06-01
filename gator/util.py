"""Utility functions"""

from gator import constants
from gator import files

import json
import os


def verify_gatorgrader_home(current_gatorgrader_home):
    """Verifies that the GATORGRADER_HOME variable is set correctly"""
    # assume that the home is not verified and try to prove otherwise
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
    """Returns GATORGRADER_HOME environment variable if is valid directory"""
    current_gatorgrader_home = os.environ.get(constants.environmentvariables.Home)
    # the current gatorgrader_home is acceptable, so use it
    if verify_gatorgrader_home(current_gatorgrader_home) is not False:
        gatorgrader_home = current_gatorgrader_home
    # the current gatorgrader_home is not valid, so create the
    # home for this program to be the current working directory
    else:
        gatorgrader_home = str(files.create_cwd_path())
    return gatorgrader_home


def get_human_answer(boolean_value):
    """Return a human readable response for the boolean_value"""
    if boolean_value is True:
        return "Yes"
    return "No"


def get_symbol_answer(boolean_value):
    """Return a symbol response for the boolean_value"""
    if boolean_value is True:
        return "✔"
    return "✘"


def is_json(potential_json):
    """Determines if a string is in JSON format"""
    try:
        json.loads(potential_json)
    except ValueError:
        return False
    return True


def greater_than_equal_exacted(first, second, exact=False):
    """Returns True if first >= second unless exact, then True if ==, otherwise False"""
    if not exact and first >= second:
        return True, first
    if exact and first == second:
        return True, first
    return False, first
