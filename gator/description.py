"""Utility functions to aid handling user-defined check descriptions"""

from gator import constants


def get_description_argument(args):
    """Extract the user-provided description from the provided command-line arguments."""
    return args.description


def transform_result_dictionary(args, result_dict):
    """Transform the produced check_result from the provided command-line arguments, if possible."""
    desc = get_description_argument(args)
    if desc is not None:
        result_dict[constants.results.Check] = desc
    return result_dict
