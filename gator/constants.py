"""Provide constants for reference by GatorGrader modules"""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants"""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args with "Constant_Name" or **kwargs with Constant_Name = "AnyConstantName"
    # note that this creates a constant that will
    # throw an AttributeError when attempting to redefine
    new_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return new_constants(*itertools.chain(args, kwargs.values()))


# define the arguments
arguments = create_constants("arguments", Incorrect=2, Void=[])

# define the codes for return values
codes = create_constants("codes", Error=1, Success=0)

# define the types of comments
comments = create_constants(
    "comments", Multiple_Line="multiple-line", Single_Line="single-line"
)

# define the programming languages for comment checks
languages = create_constants("languages", "Java", "Python")

# define the markdown indicators
markdown = create_constants("markdown", Paragraph="paragraph", Softbreak="softbreak")

# define the markers for files and output
markers = create_constants(
    "markers",
    Empty=b"",
    Newline="\n",
    No_Diagnostic="",
    Nothing="",
    Space=" ",
    Invalid=-1,
)

# define the names of modules in the system
# note that this only defines those modules
# that are reflectively called through their names
modules = create_constants(
    "modules",
    Display="gator.display",
    Invoke="gator.invoke",
    Report="gator.report",
    Run="gator.run",
)

# define the output formats
outputs = create_constants("outputs", Json="JSON", Text="TEXT")

# define the paths for use with Pathlib
# --> Current_Directory: this will describe a shortcut to current directory
# --> Current_Directory_Glob: will find all files (including dotfiles)
#     in the current directory
paths = create_constants("paths", Current_Directory=".", Current_Directory_Glob="*.*")

# define the names of fields in the result table
results = create_constants("results", "Check", "Outcome", "Diagnostic")
