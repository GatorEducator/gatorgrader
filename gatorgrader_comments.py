""" Utility functions that check the comments of a file """

import re

FILE_SEPARATOR = "/"

# References:
# https://stackoverflow.com/questions/15423658/regular-expression-for-single-line-comments
# https://blog.ostermiller.org/find-comment

MULTILINECOMMENT_RE = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
SINGLELINECOMMENT_RE = r'^(?:[^"/\\]|\"(?:[^\"\\]|\\.)*\"|/(?:[^/"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*//(.*)$'


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
