"""Check that a command executes without error."""

import argparse

from gator import checkers
from gator import invoke


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="ExecuteCommand",
        description="Check Provided by GatorGrader: ExecuteCommand",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required checker arguments")

    # COMMAND: the command to execute
    # REQUIRED? Yes
    required_group.add_argument(
        "--command", type=str, help="command to execute", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    # None required for this checker

    # }}}
    return parser


def parse(args):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args)


# pylint: disable=unused-argument
def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    # extract the two arguments for this check:
    # --> command is required to specify the commit count threshold
    check_parsed_arguments = parse(check_remaining_arguments)
    # Directly run the check since at least one of the argument's for it is mandatory.
    # This means that the use of check_ExecuteCommand would have already failed by this
    # point since argparse will exit the program if a command-line argument is not provided
    command = check_parsed_arguments.command
    return invoke.invoke_all_command_executes_checks(command)
