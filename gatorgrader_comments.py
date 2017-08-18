""" Utility functions that check the comments of a file """

from pathlib import Path
import re

FILE_SEPARATOR = "/"

SINGLELINECOMMENT_RE = r'^(?:[^"/\\]|\"(?:[^\"\\]|\\.)*\"|/(?:[^/"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*//(.*)$'
MULTILINECOMMENT_RE = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'


def check_file_in_directory(given_file, containing_directory):
    """ Returns true if the specified file is in the directory """
    file_for_checking = Path(containing_directory + FILE_SEPARATOR +
                             given_file)
    return file_for_checking.is_file()


def count_singleline_java_comment(contents):
    """ Counts the number of singleline Java comments in the code """
    pattern = re.compile(SINGLELINECOMMENT_RE, re.MULTILINE)
    matches = pattern.findall(contents)
    return len(matches)


def count_multiline_java_comment(contents):
    """ Counts the number of multiline Java comments in the code """
    pattern = re.compile(MULTILINECOMMENT_RE, re.MULTILINE)
    matches = pattern.findall(contents)
    return len(matches)
