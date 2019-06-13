"""Determines the correct exit codes to help GatorGrader quit."""


def get_code(return_values):
    """Get the correct exit code for all of the return values"""
    if False in return_values:
        return 1
    return 0
