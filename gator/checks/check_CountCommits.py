"""Check that a repository has the required number of commits."""

from gator import constants

import argparse


def parse(args):
    """Parse the arguments provided on the command-line."""
    # create the parser with the default help formatter
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Required "Optional" Arguments {{{

    # COUNT: the number of commits
    # REQUIRED? Yes
    # CORRECT WHEN: it is a number
    parser.add_argument(
        constants.commandlines.Checker_Dir,
        metavar=constants.metavars.Dir,
        help=constants.help.Checker_Dir,
        type=str,
    )

    # }}}

    # Positional Arguments {{{

    # CHECK: the name of the check
    # REQUIRED? Yes
    # CORRECT WHEN: always, selects a check and asks it to verify its own arguments
    parser.add_argument(
        constants.commandlines.Check,
        metavar=constants.metavars.Check,
        help=constants.help.Check,
        type=str,
    )

    # }}}

    # call argparse's parse_args function and return result
    arguments_finished = parser.parse_args(args)
    return arguments_finished

