"""Handle the arguments provided to GatorGrader."""

from gator import constants

import argparse


def parse(args):
    """Parse the arguments provided on the command-line."""
    # create the parser with the default help formatter
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # NOWELCOME: do not display the welcome message?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes output on screen
    gg_parser.add_argument(
        "--nowelcome", help="do not display the welcome message", action="store_true"
    )

    # JSON: output reports in JSON?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes report output
    gg_parser.add_argument("--json", help="print reports in JSON", action="store_true")

    # Positional Arguments {{{

    # CHECK: the name of the check
    # REQUIRED? Yes
    # CORRECT WHEN: always, selects a check and asks it to verify arguments further
    gg_parser.add_argument("check", help="check to run on technical writing or source code", type=str)

    # }}}

    # call argparse's parse_args function and return result
    gg_arguments_finished = gg_parser.parse_args(args)
    return gg_arguments_finished


def verify(args):
    """Check if the arguments are correct."""
    # assume that the arguments are not valid and prove otherwise
    verified_arguments = False
    return verified_arguments
