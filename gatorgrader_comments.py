""" Utility functions that check the comments of a file """

from pathlib import Path
import re

FILE_SEPARATOR = "/"

SINGLELINECOMMENT_RE = r'^(?:[^"/\\]|\"(?:[^\"\\]|\\.)*\"|/(?:[^/"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*//(.*)$'


def check_file_in_directory(given_file, containing_directory):
    """ Returns true if the specified file is in the directory """
    file_for_checking = Path(containing_directory + FILE_SEPARATOR +
                             given_file)
    return file_for_checking.is_file()


def count_singleline_java_comment(contents):
    """ Counts the number of singleline Java comments in the code """
    pattern = re.compile(SINGLELINECOMMENT_RE)
    matches = pattern.findall(contents)
    return len(matches)
