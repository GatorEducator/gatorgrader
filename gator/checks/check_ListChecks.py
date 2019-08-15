"""List the internal and external checks available through pluginbase."""

import argparse

from gator import checkers

# import snoop
# snoop.install(color="rrt")


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
        help="filter by label that name must contain",
        type=str,
    )

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    checkers.parse(get_parser, args, parser)


def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    check_parsed_arguments = parse(check_remaining_arguments)
    print(check_parsed_arguments)
    # get the source of all the checkers available from either:
    # --> the internal directory of checkers (e.g., "./gator/checks")
    # --> the directory specified on the command-line
    external_checker_directory = checkers.get_checker_dir(main_parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    # TODO: filter the names of checks with check_parsed_arguments?
    help_messages = checkers.get_checks_help(checker_source)
    return help_messages
