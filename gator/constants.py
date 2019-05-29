"""Provide constants for reference by GatorGrader modules"""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants"""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args or **kwargs ConstantName = "ConstantName"
    new_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return new_constants(*itertools.chain(args, kwargs.values()))


# define the programming languages for comment checks
languages = create_constants("languages", "Java", "Python")

# define the markers for files and output
markers = create_constants(
    "markers", Empty=b"", No_Diagnostic="", Nothing="", Space=" ", Success=0
)

# define the types of comments
comments = create_constants(
    "comments", Multiple_Line="multiple-line", Single_Line="single-line"
)
