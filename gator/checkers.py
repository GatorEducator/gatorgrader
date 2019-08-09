"""Load checkers using a plugin-based approach."""

from pluginbase import PluginBase


def get_source(checker_paths=[]):
    """Load all of the checkers."""
    checker_base = PluginBase(package="gator.checks")
    all_checker_paths = checker_paths + ["./gator/checks"] + checker_paths
    checker_source = checker_base.make_plugin_source(searchpath=all_checker_paths)
    return checker_source
