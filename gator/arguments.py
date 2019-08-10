"""Handle the top-level command-line arguments provided to GatorGrader."""

from gator import constants

import argparse


def parse(args):
    """Parse the arguments provided on the command-line."""
    # create the parser with the default help formatter
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Optional Arguments {{{

    # NOWELCOME: do not display the welcome message?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes output on screen
    gg_parser.add_argument(
        constants.commandlines.No_Welcome,
        help=constants.help.No_Welcome,
        action="store_true",
    )

    # JSON: output reports in JSON?
    # REQUIRED? No
    # CORRECT WHEN: always, only changes report output
    gg_parser.add_argument(
        constants.commandlines.Json, help=constants.help.Json, action="store_true"
    )

    # }}}

    # Positional Arguments {{{

    # CHECK: the name of the check
    # REQUIRED? Yes
    # CORRECT WHEN: always, selects a check and asks it to verify its own arguments
    gg_parser.add_argument(
        constants.commandlines.Check,
        metavar=constants.metavars.Check,
        help=constants.help.Check,
        type=str,
    )

    # }}}

    # call argparse's parse_args function and return result
    gg_arguments_finished = gg_parser.parse_args(args)
    return gg_arguments_finished


def verify(args):
    """Check if the arguments are correct."""
    # assume that the arguments are not valid and prove otherwise
    verified_arguments = False
    if args.check is not None:
        verified_arguments = True
    return verified_arguments
