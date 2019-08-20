"""List the internal and external checks available through pluginbase."""

import argparse

from gator import checkers
from gator import constants
from gator import invoke

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
    return checkers.parse(get_parser, args, parser)


def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    check_parsed_arguments = parse(check_remaining_arguments)
    # get the source of all the checkers available from either:
    # --> the internal directory of checkers (e.g., "./gator/checks")
    # --> the directory specified on the command-line
    external_checker_directory = checkers.get_checker_dir(main_parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    # must filter the names of checks with check_parsed_arguments.namecontains filter
    # verification of the arguments is necessary because --namecontains is optional
    # and there is no suitable default value for this command-line argument
    if checkers.verify_arguments_not_none(
        [check_parsed_arguments, check_parsed_arguments.namecontains]
    ):
        help_messages = checkers.get_checks_help(
            checker_source, namecontains=check_parsed_arguments.namecontains
        )
    # no need to filter the help menus based on name containment
    else:
        help_messages = checkers.get_checks_help(checker_source)
    # there is no diagnostic message because this check always passes
    diagnostic = constants.markers.Nothing
    did_check_pass = True
    # use invoke to create a report that can be returned as output
    invoke.report_result(did_check_pass, help_messages, diagnostic)
    return [did_check_pass]
