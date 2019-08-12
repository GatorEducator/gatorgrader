"""Check that a repository has the required number of commits."""

from gator import constants

import argparse

# import snoop
# snoop.install(color="rrt")


def parse(args):
    """Parse the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="CHECK: CountCommits",
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("Required Checker Arguments")

    # COUNT: the number of commits
    # REQUIRED? Yes
    required_group.add_argument(
        "--count", type=int, help="minimum number of git commits", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    # EXACT: perform exact checking for commit counts (i.e,. "==" instead of ">=")
    # REQUIRED? No
    required_group.add_argument(
        "--exact", help="equals instead of a minimum number", action="store_true"
    )

    # }}}

    # call argparse's parse_args function and return result
    arguments_finished = parser.parse_args(args)
    return arguments_finished
