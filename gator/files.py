"""Utility functions that check the contents of the file system"""

from pathlib import Path


def check_file_in_directory(given_file, home_prefix, containing_directory):
    """Returns true if the specified file is in the directory"""
    # always use a Path from pathlib to ensure platform independence
    # create the Path for the home_prefix
    home_prefix_path = Path(home_prefix)
    # create the Path for the containing directory
    containing_directory_path = Path(containing_directory)
    # create the Path for the given file
    given_file_path = Path(given_file)
    # create the Path file for checking
    # Since home_prefix_path and containing_directory_path are both absolute,
    # the code must make the containing_directory_path relative by stripping
    # off its anchor, allowing paths to be joined on all operating systems
    # pylint: disable=old-division
    file_for_checking_path = (
        home_prefix_path
        / containing_directory_path.relative_to(containing_directory_path.anchor)
        / given_file_path
    )
    return file_for_checking_path.is_file()
