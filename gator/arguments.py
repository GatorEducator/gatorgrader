"""Handle the top-level command-line arguments provided to GatorGrader."""

from gator import checkers
from gator import constants
from gator import display
from gator import files

import argparse


class GatorGraderArgumentParser(argparse.ArgumentParser):
    """Create a subclass of ArgumentParser that improves the help display."""

    def print_help(self, status=1, message=None):
        """Print the standard help message and then list the checkers."""
        # display the standard help message
        super().print_help()
        # Get all of the checks available through pluginbase.
        # Note that the "--checkdir" is not available because
        # when argparse recognizes "--help" the parse is not
        # completed. This means that this function can only
        # display those internal checks through pluginbase.
        checker_source = checkers.get_source()
        help_messages = checkers.get_checks_help(
            checker_source, indent=constants.markers.Indent
        )
        # display a blank line, a label, and then the collected
        # help messages from the internal checks through pluginbase
        display.line()
        display.line("internal checks:")
        display.line(help_messages)


def parse(args):
    """Parse the arguments provided on the command-line."""
    # create the parser with the raw test help formatter
    # that will maintain the newlines and spaces in the epilog
    # parser = argparse.ArgumentParser(
    parser = GatorGraderArgumentParser(
        prog=constants.program.Name, formatter_class=argparse.RawTextHelpFormatter
    )

    # assign a label to indicate that there is only one
    # required argument; also use "required" instead of "positional"
    parser._positionals.title = "required argument"

    # Optional Arguments {{{

    # CHECKERDIR: the directory of user-provided checkers
    # REQUIRED? No
    # CORRECT WHEN: it is a valid directory
    parser.add_argument(
        constants.commandlines.Checker_Dir,
        metavar=constants.metavars.Dir,
        help=constants.help.Checker_Dir,
        type=str,
    )

    # JSON: output reports in JSON?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes report output
    parser.add_argument(
        constants.commandlines.Json, help=constants.help.Json, action="store_true"
    )

    # NOWELCOME: do not display the welcome message?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes output on screen
    parser.add_argument(
        constants.commandlines.No_Welcome,
        help=constants.help.No_Welcome,
        action="store_true",
    )

    # }}}

    # Required Positional Argument {{{

    # CHECK: the name of the check (e.g., CheckCommits or, optionally ListChecks)
    # REQUIRED? Yes
    # CORRECT WHEN: always, selects a check and asks it to verify its own arguments
    parser.add_argument(
        constants.commandlines.Check,
        metavar=constants.metavars.Check,
        help=constants.help.Check,
        type=str,
    )

    # }}}

    # add an epilog to explain how to list all of the available checks,
    # including those checks that are internal and user-provided
    parser.epilog = "all checks:\r\n  list all available checks with CHECK as ListChecks\r\n  usage: gatorgrader.py ListChecks"
    # call argparse's parse_known_args function that will recognize all
    # matching arguments and those that remain to be parsed and return them both
    arguments_finished, arguments_remaining = parser.parse_known_args(args)
    return arguments_finished, arguments_remaining


def verify(args):
    """Check if the arguments are correct."""
    # assume the arguments are valid, then prove otherwise
    verified_arguments = True
    # CHECKERDIR: an external directory of checks was specified
    # ENSURE: this directory is a valid directory
    if args.checkerdir is not None:
        # assume that it is not a valid directory, then prove otherwise
        verified_arguments = False
        checkerdir_path = files.create_path(file="", home=args.checkerdir)
        # the directory does exist, so this argument is verified
        if checkerdir_path.is_dir():
            verified_arguments = True
    return verified_arguments
