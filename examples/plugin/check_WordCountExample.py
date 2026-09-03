"""Example external checker: count the total number of words in a file."""

import argparse
import os

from gator import checkers, invoke


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    parser = argparse.ArgumentParser(
        prog="WordCountExample",
        description="Example check: count words in a file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    required_group = parser.add_argument_group("required checker arguments")

    required_group.add_argument(
        "--file", type=str, help="file for checking", required=True
    )

    required_group.add_argument(
        "--directory",
        type=str,
        metavar="DIR",
        help="directory with file for checking",
        required=True,
    )

    required_group.add_argument(
        "--count", type=int, help="expected total word count", required=True
    )

    return parser


def parse(args):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args)


def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    check_parsed_arguments = parse(check_remaining_arguments)
    count = check_parsed_arguments.count
    file = check_parsed_arguments.file
    directory = check_parsed_arguments.directory

    filepath = os.path.join(directory, file)
    with open(filepath, "r", encoding="utf-8") as fh:
        total_words = len(fh.read().split())

    passed = total_words >= count
    if passed:
        invoke.report_result(
            True, f"File contains {total_words} words (>= {count})", None
        )
    else:
        invoke.report_result(
            False,
            f"File contains {total_words} words, expected at least {count}",
            f"Found {total_words} words, expected >= {count}",
        )
    return passed
