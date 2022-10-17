"""Load checkers using a plugin-based approach."""

import io
from contextlib import redirect_stdout

import pkgutil
import importlib
import os

from gator import checks
from gator import constants
from gator.exceptions import InvalidCheckArgumentsError

from pluginbase import PluginBase

CHECKER_SOURCE = None

DEFAULT_FUNCTIONS = [
    constants.checkers.Function_Act,
    constants.checkers.Function_Get_Parser,
    constants.checkers.Function_Parse,
]


def parse(get_parser, args):
    """Use the parser on the provided arguments."""
    # this function is called by all checks in gator.checks
    # get the provided parser
    parser = get_parser()
    # call provided parse_args function and return result
    # FIXME: this is a hacky way to redirect argparse's default printing behavior
    parser.print_usage = lambda _file: None

    # redirect exit reason to msg
    def exit_raise(_status, message=None):
        raise InvalidCheckArgumentsError(
            args, parser.format_usage(), message, parser.prog
        )

    parser.exit = exit_raise

    return parser.parse_args(args)


def get_checker_dir(args):
    """Extract the checker directory from the provided command-line arguments."""
    # assume that the checkerdir does not exist and re-assign if found
    checker_directory = constants.markers.Nothing
    # the checkerdir was specified and thus it should be returned
    if args.checkerdir is not None:
        checker_directory = args.checkerdir
    return checker_directory


def get_chosen_check(args):
    """Extract the chosen check from the provided command-line arguments."""
    # GatorGrader's argument parser will store the specified check in the
    # check variable inside of the provided args; access this and return it
    chosen_check = args.check
    return chosen_check


def transform_check(check):
    """Transform the chosen check from the provided command-line arguments."""
    # add "check_" to the name of the checker so that it looks like, for instance,
    # "check_CountCommits" when "CountCommits" is chosen on command-line
    transformed_check = constants.checkers.Check_Prefix + check
    return transformed_check


def verify_arguments_not_none(args):
    """Verify that the provided arguments are all not None."""
    # assume that you have not found a None yet
    found_none = False
    # iteratively look for a None through the arguments
    for arg in args:
        # indicate that a None was found
        # stop running the for loop since None's existence is established;
        # this short-circuit behavior also ensure that the function works
        # when you are checking that an object is not None so that you
        # can then access a field inside of that object
        if arg is None:
            found_none = True
            break
    # if a None was found, then do not verify the arguments
    return not found_none


def verify_check_existence(check, check_source):
    """Verify that the requested check is available from the source(s)."""
    check_exists = False
    # list each of the checks by name as they are available in the
    # --> internal source that comes with GatorGrader
    # --> the external source specified by user on the command-line
    check_list = list_checks(check_source)
    # if the name of the check is in the list of plugins
    # then we can confirm its existence
    if check in check_list:
        check_exists = True
    return check_exists


def verify_check_function(check, function):
    """Verify that the requested check has a function."""
    # the specified check, a module loaded by pluginbase, has the specified function
    if hasattr(check, function):
        return True
    # the specified check does not have the function, so do not verify it
    return False


def verify_check_functions(check, functions=DEFAULT_FUNCTIONS):
    """Verify that the requested check has the required functions."""
    # perform verification on the specified check, a module loaded by pluginbase,
    # for all of the provided functions, which are, DEFAULT_FUNCTIONS by default
    verify_status_results = [
        verify_check_function(check, function) for function in functions
    ]
    # verify the status of the check as long as all values in verify_status_results are True
    return all(verify_status_results)


def is_internal_check(check_file):
    """Determine if the specified check is an internal check."""
    return check_file in list_checks(None)


def list_checks(checker_source):
    """List the available checks from the source."""
    all_checks = []
    for moduleInfo in pkgutil.walk_packages(checks.__path__):
        all_checks.append(moduleInfo.name)
    if checker_source:
        all_checks.extend(checker_source.list_plugins())
    return all_checks


def load_check(checker_source, check_file):
    """Load the specified check from the source."""
    if is_internal_check(check_file):
        return importlib.import_module(checks.__name__ + "." + check_file)
    else:
        return checker_source.load_plugin(check_file)


def get_source(checker_paths=[]):
    """Load all of the checkers using pluginbase."""
    # define the "package" in which the checks reside
    # the term "package" corresponds to "module.sub-module"
    checker_base = PluginBase(package=constants.packages.Checks)
    # remove any directories from the path listings that are Nothing (i.e., "")
    # this case occurs when the optional --checkerdir is not provided on command-line
    if constants.markers.Nothing in checker_paths:
        checker_paths.remove(constants.markers.Nothing)
    # Create and return a source of checkers using PluginBase.
    # The documentation for this function advices that you
    # give an identifier to the source for the plugins
    # because this will support saving and transfer, if needed.
    # Only perform this operation if the checker source is None,
    # meaning that it has not already been initialized.
    # pylint: disable=global-statement
    global CHECKER_SOURCE
    if CHECKER_SOURCE is None:
        CHECKER_SOURCE = checker_base.make_plugin_source(
            identifier=constants.checkers.Plugin_Base_Identifier,
            searchpath=checker_paths,
        )
    return CHECKER_SOURCE


def reset_source():
    """Reset the source of the checkers."""
    # pylint: disable=global-statement
    global CHECKER_SOURCE
    # if the checker source was previously created, then
    # cleanup all of the state from that source and then
    # reset it to None to indicate it must be re-created
    if CHECKER_SOURCE is not None:
        CHECKER_SOURCE.cleanup()
        CHECKER_SOURCE = None


def get_check_help(active_check, indent=""):
    """Extract the help message from a checker available in the source from pluginbase."""
    # assume that the active check does not have a help message
    active_check_parser_help = constants.markers.Nothing
    # the active check has a function to get the parser
    if hasattr(active_check, constants.checkers.Function_Get_Parser):
        active_check_parser = active_check.get_parser()
        # extract the help message by redirecting standard output to a string
        with io.StringIO() as buffer, redirect_stdout(buffer):
            active_check_parser.print_help()
            active_check_parser_help = buffer.getvalue()
    # delete blank lines from the help message to improve formatting
    # note that if there were no valid checks, then active_check_parser_help
    # will not contain any content (i.e., it is constants.markers.Nothing)
    # and thus this next line of code will still result in the same Nothing
    active_check_parser_help = os.linesep.join(
        [indent + line for line in active_check_parser_help.splitlines() if line]
    )
    return active_check_parser_help


def get_checks_help(check_source, namecontains=None, indent=""):
    """Extract the help message from all checkers available in the source from pluginbase."""
    # assume that no checkers are available and thus there is no help message
    help_message = constants.markers.Nothing
    # extract the list of checkers available from pluginbase
    check_list = list_checks(check_source)
    # a namecontains is provided for the filtering to ensure that each check
    # contains the provided name pattern (i.e., must contain "Comment")
    filtered_check_list = check_list
    if namecontains is not None:
        filtered_check_list = [
            check_name
            for check_name in check_list
            if namecontains.casefold() in check_name.casefold()
        ]
    # iterate through the names of the checks, extracting their help messages
    for check_count, check_file in enumerate(filtered_check_list):
        # reflectively create a check from its name
        active_check = load_check(check_source, check_file)
        # if possible, get the complete help message from this check
        active_check_parser_help = get_check_help(active_check, indent)
        # this is the first help message, so directly add it
        if help_message is constants.markers.Nothing:
            # this is the only help message, so add it without a blank line
            if check_count == len(filtered_check_list) - 1:
                help_message = active_check_parser_help
            # there are other help messages, so add a blank line to separate
            else:
                help_message = active_check_parser_help + constants.markers.Newline
        # there are one or more help messages, so separate and then add this one
        # to the running help message. This would form a full help message like:
        # HELP-MESSAGE-1 BLANK-LINE HELP-MESSAGE-2 BLANK-LINE ... HELP-MESSAGE-n
        # for a total of n HELP-MESSAGES for the n available checkers in pluginbase
        else:
            # this is the last check so do not add the trailing blank line
            if check_count == len(filtered_check_list) - 1:
                help_message = (
                    help_message + constants.markers.Newline + active_check_parser_help
                )
            # this is not last check so add the trailing blank line
            else:
                help_message = (
                    help_message
                    + constants.markers.Newline
                    + active_check_parser_help
                    + constants.markers.Newline
                )
    return help_message
