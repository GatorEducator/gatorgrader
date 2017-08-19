""" Utility functions that check the comments of a file """

from pathlib import Path
import re

FILE_SEPARATOR = "/"

SINGLELINECOMMENT_RE = r'^(?:[^"/\\]|\"(?:[^\"\\]|\\.)*\"|/(?:[^/"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*//(.*)$'
MULTILINECOMMENT_RE = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'


def entities_greater_than_count(given_file, containing_directory,
                                expected_count, checking_function):
    """ Determines in the entity count is greater than expected """
    file_entity_count = count_entities(given_file, containing_directory,
                                       checking_function)
    if file_entity_count >= expected_count:
        return True
    return False


def count_entities(given_file, containing_directory, checking_function):
    """ Counts the number of entities for the file in the directory """
    file_for_checking = Path(containing_directory + FILE_SEPARATOR +
                             given_file)
    file_contents_count = 0
    if file_for_checking.is_file():
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents)
    return file_contents_count


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
