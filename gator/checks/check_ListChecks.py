"""List the internal and external checks available through pluginbase."""

import argparse

from gator import checkers


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="ListChecks",
        description="Check Provided by GatorGrader: ListChecks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    # None required for this checker

    # }}}

    # Optional Named Checker Arguments {{{

    optional_group = parser.add_argument_group("optional check arguments")

    # NAMECONTAINS: label for filtering the checks by name
    # REQUIRED? No
    optional_group.add_argument(
        "--namecontains",
        metavar="LABEL",
        help="filter checks by a label that a check's name must contain",
        type=str,
    )

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    checkers.parse(get_parser, args, parser)
