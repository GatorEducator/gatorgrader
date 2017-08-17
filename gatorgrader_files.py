""" Utility functions that check the contents of the file system """

from pathlib import Path

FILE_SEPARATOR = "/"


def check_file_in_directory(given_file, containing_directory):
    """ Returns true if the specified file is in the directory """
    print("containing dir", containing_directory)
    print("given file", given_file)
    file_for_checking = Path(containing_directory + FILE_SEPARATOR +
                             given_file)
    return file_for_checking.is_file()
