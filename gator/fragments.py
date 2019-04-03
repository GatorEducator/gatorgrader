"""Retrieve and count the contents of a file"""

from pathlib import Path

import commonmark
import re

from gator import util

FILE_SEPARATOR = "/"

NEWLINE = "\n"
NOTHING = ""
SPACE = " "


def get_paragraphs(contents):
    """Retrieves the paragraphs in the writing"""
    ast = commonmark.Parser().parse(contents)
    mode_looking = True
    paragraph_list = []
    paragraph_content = ""
    counter = 0

    # Iterate through the markdown to find paragraphs and add their contents to paragraph_list
    for subnode, enter in ast.walker():
        if mode_looking:
            # Check to see if the current subnode is an open paragraph node
            if counter == 1 and subnode.t == "paragraph" and enter:
                # Initialize paragraph_content
                paragraph_content = ""
                # Stop search for paragraph nodes, as one has been found
                # Instead, start adding content to paragraph_content
                mode_looking = False
        else:
            # Check to see if the current subnode is a closing paragraph node
            if counter == 2 and subnode.t == "paragraph" and not enter:
                # Add the content of the paragraph to paragraph_list
                paragraph_list.append(paragraph_content)
                # Stop saving paragraph contents, as the paragraph had ended
                # Start a search for a new paragraph
                mode_looking = True
            # If the subnode literal has contents, add them to paragraph_content
            if subnode.literal is not None:
                paragraph_content += subnode.literal

        # Track the how deep into the tree the search currently is
        if subnode.is_container():
            if enter:
                counter += 1
            else:
                counter -= 1

    return paragraph_list


def get_line_list(content):
    """Returns a list of lines from any type of input string"""
    actual_content = []
    # iteratively decode each of the lines in the content
    for line in content.splitlines(keepends=False):
        # decode worked for this content and charset, use decoded
        try:
            current_line_decoded = line.decode()
        # decode worked for this content and charset, use line
        except AttributeError:
            current_line_decoded = line
        # the decoded line is not a blank space (e.g., "")
        # so it should be added into the list of lines
        # the goal is to avoid counting blank lines
        if not is_blank_line(current_line_decoded):
            actual_content.append(current_line_decoded)
    return actual_content


def is_blank_line(line):
    """Returns True if a line is a blank one and False otherwise"""
    if line is not None and line is not NOTHING and not line.isspace():
        return False
    return True


def count_paragraphs(contents):
    """Counts the number of paragraphs in the writing"""
    matching_paragraphs = get_paragraphs(contents)
    return len(matching_paragraphs)


def count_words(contents):
    """Counts the minimum number of words across all paragraphs in writing"""
    # retrieve all of the paragraphs in the contents
    paragraphs = get_paragraphs(contents)
    # count all of the words in each paragraph
    word_counts = []
    for para in paragraphs:
        para = para.replace(NEWLINE, SPACE)
        words = NOTHING.join(ch if ch.isalnum() else SPACE for ch in para).split()
        word_counts.append(len(words))
    # return the minimum number of words across all paragraphs
    if word_counts:
        return min(word_counts)
    # counting did not work correctly, so return 0
    return 0


def count_specified_fragment(contents, fragment):
    """Counts the specified string fragment in the string contents"""
    fragment_count = contents.count(fragment)
    return fragment_count


def count_specified_regex(contents, regex):
    """Counts all the specified regex for a given file"""
    # finds regex matches, returns their count
    if not is_valid_regex(regex):
        return -1

    matches = re.findall(regex, contents, re.DOTALL)
    return len(matches)


# pylint: disable=bad-continuation
def specified_entity_greater_than_count(
    chosen_fragment,
    checking_function,
    expected_count,
    given_file=NOTHING,
    containing_directory=NOTHING,
    contents=NOTHING,
    exact=False,
):
    """Determines if the entity count is greater than expected"""
    # count the fragments/regex in either a file in a directory or String contents
    file_entity_count = count_entities(
        chosen_fragment, checking_function, given_file, containing_directory, contents
    )
    # check the condition and also return file_entity_count
    return util.greater_than_equal_exacted(file_entity_count, expected_count, exact)


# pylint: disable=bad-continuation
def count_entities(
    chosen_fragment,
    checking_function,
    given_file=NOTHING,
    containing_directory=NOTHING,
    contents=NOTHING,
):
    """Counts fragments for the file in the directory (or contents) and a fragment"""
    file_for_checking = Path(containing_directory + FILE_SEPARATOR + given_file)
    file_contents_count = 0
    # file is not available and the contents are provided
    if not file_for_checking.is_file() and contents is not NOTHING:
        file_contents_count = checking_function(contents, chosen_fragment)
    # file is available and the contents are not provided
    elif file_for_checking.is_file() and contents is NOTHING:
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents, chosen_fragment)
    return file_contents_count


# pylint: disable=bad-continuation
def specified_source_greater_than_count(
    expected_count,
    given_file=NOTHING,
    containing_directory=NOTHING,
    contents=NOTHING,
    exact=False,
):
    """Determines if the line count is greater than expected"""
    # count the fragments in either a file in a directory or String contents
    file_line_count = count_lines(given_file, containing_directory, contents)
    # the fragment count is at or above the threshold
    # check the condition and also return file_fragment_count
    return util.greater_than_equal_exacted(file_line_count, expected_count, exact)


def count_lines(given_file=NOTHING, containing_directory=NOTHING, contents=NOTHING):
    """Counts lines for the file in the directory (or contents)"""
    file_for_checking = Path(containing_directory + FILE_SEPARATOR + given_file)
    file_contents_count = 0
    # file is not available and the contents are provided
    if not file_for_checking.is_file() and contents is not NOTHING:
        line_list = get_line_list(contents)
        file_contents_count = len(line_list)
    # file is available and the contents are not provided
    elif file_for_checking.is_file() and contents is NOTHING:
        file_contents = file_for_checking.read_text()
        line_list = get_line_list(file_contents)
        file_contents_count = len(line_list)
    return file_contents_count


def is_valid_regex(regex):
    """Determines if regex is valid"""
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
