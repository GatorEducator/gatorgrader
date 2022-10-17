"""Determine the correct exit code to help GatorGrader quit."""

from gator import constants


def get_code(passed):
    """Get the correct exit code."""
    return constants.codes.Success if passed else constants.codes.Error
