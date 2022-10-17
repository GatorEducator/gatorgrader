"""Check that a command's output matches a specified regular expression."""

import argparse

from gator import checkers
from gator import invoke


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="MatchCommandRegex",
        description="Check Provided by GatorGrader: MatchCommandRegex",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required checker arguments")

    # COMMAND: the command to execute
    # REQUIRED? Yes
    required_group.add_argument(
        "--command", type=str, metavar="CMD", help="command to execute", required=True
    )

    # REGEX: the regular expression that should match the command's output
    # REQUIRED? Yes
    required_group.add_argument(
        "--regex",
        type=str,
        help="regular expression that matches command output",
        required=True,
    )

    # COUNT: the number of regular expression matches
    # REQUIRED? Yes
    required_group.add_argument(
        "--count", type=int, help="how many regex matches should exist", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    optional_group = parser.add_argument_group("optional check arguments")

    # EXACT: perform exact checking for commit counts (i.e,. "==" instead of ">=")
    # REQUIRED? No
    optional_group.add_argument(
        "--exact",
        help="equals instead of a minimum number",
        default=False,
        action="store_true",
    )

    # }}}
    return parser


def parse(args):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args)


# pylint: disable=unused-argument
def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    # extract the two arguments for this check:
    # --> command is required to specify the command to perform
    # --> regex is the regular expression that should match the command's output
    # --> count is required to specify the number of matches in regular expressions
    # --> exact is optional, but will either be True or False and False by default
    check_parsed_arguments = parse(check_remaining_arguments)
    # Directly run the check since at least one of the argument's for it is mandatory.
    # This means that the use of check_MatchCommandRegex would have already failed by this
    # point since argparse will exit the program if a command-line argument is not provided.
    command = check_parsed_arguments.command
    regex = check_parsed_arguments.regex
    count = check_parsed_arguments.count
    exact = check_parsed_arguments.exact
    return invoke.invoke_all_command_regex_checks(command, regex, count, exact)
