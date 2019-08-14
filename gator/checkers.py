"""Load checkers using a plugin-based approach."""

from gator import constants

from pluginbase import PluginBase

import io
from contextlib import redirect_stdout

# import snoop
# snoop.install(color="rrt")


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
    # create and return a source of checkers using PluginBase
    # the documentation for this function advices that you
    # give an identifier to the source for the plugins
    # because this will support saving and transfer, if needed
    checker_source = checker_base.make_plugin_source(
        identifier=constants.checkers.Plugin_Base_Identifier,
        searchpath=all_checker_paths,
    )
    return checker_source


def get_check_help(check_source):
    """Extract the help message from each checker available in the source from pluginbase."""
    help_message = ""
    check_list = check_source.list_plugins()
    for check_name in check_list:
        active_check = check_source.load_plugin(check_name)
        if hasattr(active_check, 'get_parser'):
            active_check_parser = active_check.get_parser()
        with io.StringIO() as buf, redirect_stdout(buf):
            active_check_parser.print_help()
            active_check_parser_help = buf.getvalue()
            help_message = active_check_parser_help
    return help_message
