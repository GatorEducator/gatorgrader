"""Confirm that a file exists in a directory."""

import argparse

from gator import checkers
from gator import invoke


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="ConfirmFileExists",
        description="Check Provided by GatorGrader: ConfirmFileExists",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required checker arguments")

    # FILE: the file
    # REQUIRED? Yes
    required_group.add_argument(
        "--file", type=str, help="file for checking", required=True
    )

    # DIRECTORY: the directory containing the file
    # REQUIRED? Yes
    required_group.add_argument(
        "--directory",
        type=str,
        metavar="DIR",
        help="directory with file for checking",
        required=True,
    )

    # }}}

    # Optional Named Checker Arguments {{{

    optional_group = parser.add_argument_group("optional check arguments")

    # None required for this checker
    # REACH: allows for a students to have a reach goal in their lab/practical
    # REQUIRED? No
    optional_group.add_argument(
        "--reach",
        help="creates a higher goal for students to potentially reach",
        default=False,
        action="store_true",
    )

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args, parser)


# pylint: disable=unused-argument
def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    # extract the two arguments for this check:
    # --> file is the name of the file for which the search is conducted
    # --> directory is the name of the directory that should contain the specified file
    check_parsed_arguments = parse(check_remaining_arguments)
    # Directly run the check since at least one of the argument's for it is mandatory.
    # This means that the use of check_ConfirmFileExists would have already failed by this
    # point since argparse will exit the program if a command-line argument is not provided
    file = check_parsed_arguments.file
    directory = check_parsed_arguments.directory
    reach = check_parsed_arguments.reach
    return [invoke.invoke_file_in_directory_check(file, directory)]
