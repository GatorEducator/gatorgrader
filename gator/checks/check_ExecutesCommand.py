"""Check that a command executes without error."""

import argparse

from gator import checkers


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="ExecutesCommand",
        description="Check Provided by GatorGrader: ExecutesCommand",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required checker arguments")

    # COUNT: the number of commits
    # REQUIRED? Yes
    required_group.add_argument(
        "--command", type=str, help="command to execute", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    # None required for this checker

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    checkers.parse(get_parser, args, parser)
