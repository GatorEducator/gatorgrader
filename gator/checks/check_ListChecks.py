"""List the internal and external checks available through pluginbase."""

import argparse

from gator import checkers
from gator import constants
from gator import invoke


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
    # create a label that explains the meaning of the check
    label = "Find the available checks that match an optional pattern"
    # there were no checks that matched, which means:
    # --> only the label is display, without any help messages
    # --> the diagnostic should indicate that the search failed
    # --> the check "failed", ensuring that the diagnostic appears
    if help_messages is constants.markers.Nothing:
        help_messages = label
        diagnostic = "Could not find any matching checks"
        did_check_pass = False
    # there were checks that matched, which means:
    # --> the label is display, then newlines, and then all matching help messages
    # --> the diagnostic should not appear since the search succeeded
    else:
        # add a label to the first line of the help messages
        # then add a blank line and then add the messages themselves
        help_messages = (
            label
            + constants.markers.Newline
            + constants.markers.Newline
            + help_messages
        )
        # there is no diagnostic message because this check passed
        diagnostic = constants.markers.Nothing
        did_check_pass = True
    # use invoke to create a report that can be returned as output
    invoke.report_result(did_check_pass, help_messages, diagnostic)
    return did_check_pass
