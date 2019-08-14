"""Load checkers using a plugin-based approach."""

from gator import constants

from pluginbase import PluginBase

import io
from contextlib import redirect_stdout

# import snoop
# snoop.install(color="rrt")

CHECKER_SOURCE = None


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


def verify_check_existence(check, check_source):
    """Verify that the requested check is available from the source(s)."""
    check_exists = False
    # list each of the checks by name as they are available in the
    # --> internal source that comes with GatorGrader
    # --> the external source specified by user on the command-line
    check_list = check_source.list_plugins()
    # if the name of the check is in the list of plugins
    # then we can confirm its existence
    if check in check_list:
        check_exists = True
    return check_exists


def get_source(checker_paths=[]):
    """Load all of the checkers using pluginbase."""
    # define the "package" in which the checks reside
    # the term "package" corresponds to "module.sub-module"
    checker_base = PluginBase(package=constants.packages.Checks)
    # remove any directories from the path listings that are Nothing (i.e., "")
    # this case occurs when the optional --checkerdir is not provided on command-line
    if constants.markers.Nothing in checker_paths:
        checker_paths.remove(constants.markers.Nothing)
    # create the listing of the paths that could contain checkers
    all_checker_paths = checker_paths + [constants.checkers.Internal_Checkers_Dir]
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
            searchpath=all_checker_paths,
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


def get_check_help(check_source):
    """Extract the help message from each checker available in the source from pluginbase."""
    # assume that no checkers are available and thus there is no help message
    help_message = constants.markers.Nothing
    # iterate through the list of checkers available from pluginbase
    check_list = check_source.list_plugins()
    for check_name in check_list:
        active_check = check_source.load_plugin(check_name)
        # the active check has a function to get the parser
        if hasattr(active_check, constants.checkers.Get_Parser_Function):
            active_check_parser = active_check.get_parser()
            # extract the help message by redirecting standard output to a string
            with io.StringIO() as buffer, redirect_stdout(buffer):
                active_check_parser.print_help()
                active_check_parser_help = buffer.getvalue()
                # this is the first help message, so directly add it
                if help_message is constants.markers.Nothing:
                    help_message = active_check_parser_help
                # there are one or more help messages, so separate and then add it
                else:
                    help_message = constants.markers.Newline + active_check_parser_help
    return help_message
