"""Load checkers using a plugin-based approach."""

from gator import constants

from pluginbase import PluginBase

import snoop
snoop.install(color="rrt")


@snoop
def get_sources(checker_paths=[]):
    """Load all of the checkers using pluginbase."""
    checker_base = PluginBase(package=constants.packages.Checks)
    all_checker_paths = checker_paths + ["./gator/checks"]
    checker_source = checker_base.make_plugin_source(searchpath=all_checker_paths)
    return checker_source
