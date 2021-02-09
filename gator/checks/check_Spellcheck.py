"""Check that writing in a report file is correctly spelled."""

import argparse

from gator import checkers
from gator import constants
from gator import fragments
from gator import invoke


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    parser = argparse.ArgumentParser(
        prog="Spellcheck",
        description="Check Provided by GatorGrader: Spell Checking",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Argument(s).
    required_group = parser.add_argument_group("Required checker arguments")

    # (Required) FILE: source file.
    required_group.add_argument(
        "--file", type=str, help="File for checking", required=True
    )

    # (Required) DIRECTORY: path to file.
    required_group.add_argument("--directory", type=str, metavar="DIR", required=True)

    # Optional Arguments.
    optional_group = parser.add_argument_group("Optional check arguments")

    # (Not Required) Ignore Mistakes: ignore a specific amount of spelling mistakes.
    optional_group.add_argument(
        "--ignore",
        help="Ignore a certain amount of spelling mistakes",
        default=0,
        type=int,
        required=False,
    )
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args, parser)


# pylint: disable=unused-argument
def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    # Two required arguments for this check: File and Directory Path
    # One argument is not required: Ignore Count

    check_parsed_arguments = parse(check_remaining_arguments)

    file = check_parsed_arguments.file
    directory = check_parsed_arguments.directory
    ignore_count = check_parsed_arguments.ignore
    return [invoke.invoke_spellcheck(file, directory, ignore_count,)]
