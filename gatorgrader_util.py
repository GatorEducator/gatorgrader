""" Utility functions for GatorGrader """


def get_human_answer(boolean_value):
    """Return a human readable response for the boolean_value"""
    if boolean_value is True:
        return "Yes"
    return "No"
