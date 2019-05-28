"""Provide constants for reference by GatorGrader modules"""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants"""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args or **kwargs ConstantName = "ConstantName"
    created_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return created_constants(*itertools.chain(args, kwargs.values()))


# define the programming languages for comment checks
languages = create_constants('languages', 'Java', 'Python')
