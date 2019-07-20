"""Utility functions that check the comments of a file."""

import re

from gator import constants

# References for the regular expressions:
# https://stackoverflow.com/questions/15423658/regular-expression-for-single-line-comments
# https://blog.ostermiller.org/find-comment

# define regular expressions for pattern matching
MULTILINECOMMENT_RE_JAVA = r"""/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/"""
SINGLELINECOMMENT_RE_JAVA = r"""^(?:[^"/\\]|\"(?:[^\"\\]|\\.)*
\"|/(?:[^/"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*//(.*)$"""
SINGLELINECOMMENT_RE_PYTHON = r"""^(?:[^"#\\]|\"(?:[^\"\\]|\\.)*\"|
/(?:[^#"\\]|\\.)|/\"(?:[^\"\\]|\\.)*\"|\\.)*#(.*)$"""
MULTILINECOMMENT_RE_PYTHON = r'^[ \t]*"""(.*?)"""[ \t]*$'


def count_singleline_java_comment(contents):
    """Count the number of singleline Java comments in the code."""
    pattern = re.compile(SINGLELINECOMMENT_RE_JAVA, re.MULTILINE | re.VERBOSE)
    matches = pattern.findall(contents)
    matches_count = len(matches)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_python_comment(contents):
    """Count the number of singleline Python comments in the code."""
    pattern = re.compile(SINGLELINECOMMENT_RE_PYTHON, re.MULTILINE)
    matches = pattern.findall(contents)
    matches_count = len(matches)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_java_comment(contents):
    """Count the number of multiline Java comments in the code."""
    pattern = re.compile(MULTILINECOMMENT_RE_JAVA, re.MULTILINE)
    matches = pattern.findall(contents)
    matches_count = len(matches)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_python_comment(contents):
    """Count the number of multiline Python comments in the code."""
    pattern = re.compile(MULTILINECOMMENT_RE_PYTHON, re.MULTILINE | re.DOTALL)
    matches = pattern.findall(contents)
    matches_count = len(matches)
    return matches_count, {constants.markers.First: matches_count}
