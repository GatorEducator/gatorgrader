"""Determines the correct exit codes to help GatorGrader quit"""

from gator import constants


def get_code(return_values):
    """Get the correct exit code for all of the return values"""
    # one of the return values is False,
    # meaning that this is an error code
    if False in return_values:
        return constants.codes.Error
    # none of the return values are False,
    # meaning that this is a success code
    return constants.codes.Success
