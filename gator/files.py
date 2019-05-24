"""Utility functions that check the contents of the file system"""

import pathlib
from pathlib import Path

# FILE_SEPARATOR = "/"


def check_file_in_directory(given_file, home_prefix, containing_directory):
    """Returns true if the specified file is in the directory"""
    # OLD: file_for_checking = Path(containing_directory + FILE_SEPARATOR + given_file)
    # create the Path for the home_prefix
    home_prefix_path = Path(home_prefix)
    print(str(home_prefix_path))
    # create the Path for the containing directory
    containing_directory_path = Path(containing_directory)
    print(str(containing_directory_path))
    # create the Path for the given file
    given_file_path = Path(given_file)
    print(str(given_file_path))
    # create a file for checking using the two newly created paths
    file_for_checking_path = home_prefix_path / containing_directory_path.relative_to(
        containing_directory_path.anchor
    )
    print("This is the file for checking: " + str(file_for_checking_path.absolute()))
    # print("Given file: " + given_file)
    # print("Containing directory: " + containing_directory)
    # print(
    #     "Trying to create path of " + containing_directory + FILE_SEPARATOR + given_file
    # )
    return file_for_checking_path.is_file()
