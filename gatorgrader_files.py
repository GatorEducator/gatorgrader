""" Utility functions that check the contents of the file system """

from pathlib import Path

FILE_SEPARATOR = "/"


def file_in_directory(given_file, containing_directory):
    """ Returns true if the specified file is in the directory """
    print("directory:", containing_directory)
    print("file:", given_file)
    file_for_checking = Path(containing_directory +
                             FILE_SEPARATOR + given_file)
    return file_for_checking.is_file()
