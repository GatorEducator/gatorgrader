"""Load checkers using a plugin-based approach."""

from gator import constants

from pluginbase import PluginBase

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
