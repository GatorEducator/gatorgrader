"""Provide constants for reference by GatorGrader modules."""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants."""
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
codes = create_constants("codes", Error=1, Success=0, No_Words=0)

# define details about the checkers
checkers = create_constants(
    "checkers",
    Check_Prefix="check_",
    Internal_Checkers_Dir="gator/checks",
    Function_Act="act",
    Function_Get_Parser="get_parser",
    Function_Parse="parse",
    Plugin_Base_Identifier="GatorGraderPluginBase",
)

# define the command-line arguments
# note that "--" arguments are optional
# and those without "--" are positional
commandlines = create_constants(
    "commandlines",
    Check="check",
    Checker_Dir="--checkerdir",
    Json="--json",
    List_Checks="--listchecks",
    No_Welcome="--nowelcome",
)

# define the types of comments
comments = create_constants(
    "comments", Multiple_Line="multiple-line", Single_Line="single-line"
)

# define the environment variables for the program
environmentvariables = create_constants("environmentvariables", Home="GATORGRADER_HOME")

# define reference function names in the program
functions = create_constants("functions", Count_Total_Words="count_total_words")

# define the help messages for command-line arguments
help = create_constants(
    "help",
    Check="check to perform on the writing or source code",
    Checker_Dir="directory containing user-provided checks",
    Json="print the status report in JSON",
    List_Checks="list the internal and user-provided checks",
    No_Welcome="do not display the welcome message",
)

# define the programming languages for comment checks
languages = create_constants("languages", "Java", "Python")

# define the markdown indicators
markdown = create_constants("markdown", Paragraph="paragraph", Softbreak="softbreak")

# define the markers for files and output
markers = create_constants(
    "markers",
    Arrow="➔",
    Empty=b"",
    Newline="\n",
    No_Diagnostic="",
    Nothing="",
    Space=" ",
    Indent="  ",
    Tab="   ",
    File="file",
    Of_File="of file",
    In_A_File="in a file",
    First=1,
    Invalid=-1,
)

# define the metavars
metavars = create_constants("metavars", Check="CHECK", Dir="DIR")

# define the names of modules in the system
# note that this only defines those modules
# that are reflectively called through their names
modules = create_constants(
    "modules",
    Checks="gator.checks",
    Display="gator.display",
    Invoke="gator.invoke",
    Report="gator.report",
    Run="gator.run",
)

# define the output formats
outputs = create_constants("outputs", Json="JSON", Text="TEXT")

# define the names of packages used in pluginbase
packages = create_constants("packages", Checks="gator.checks")

# define the paths for use with Pathlib:
# --> Current_Directory: this will describe a shortcut to current directory
# --> Current_Directory_Glob: will find all files (including dotfiles)
#     in the current directory
# --> Home: the name that must exist at the end of the project's home directory
paths = create_constants(
    "paths", Current_Directory=".", Current_Directory_Glob="*.*", Home="gatorgrader"
)

# define the details about the program:
# --> Name: the name of the program that is run
program = create_constants("program", Name="gatorgrader.py")

# define the names of fields in the result table
# note that the variable name can be capitalized
# however, the contents of the constant cannot be
# capitalized because the JSON report that is transmitted
# between Python and Java expects that the keys are lowercase
results = create_constants(
    "results", Check="check", Outcome="outcome", Diagnostic="diagnostic"
)

# define the version control repository details
versioncontrol = create_constants("versioncontrol", Master="master", No_Commits=[])

# define the words diagnostic messages
words = create_constants(
    "words",
    Minimum="word(s) in every paragraph",
    Total="word(s) in total",
    In_A="in a",
    In_Every="in every",
    In_The="in the",
    Cardinal="cardinal",
    Ordinal="ordinal",
    Paragraph="paragraph",
)
