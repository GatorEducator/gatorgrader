"""Retrieve and count the contents of a file"""

import re
import commonmark

from gator import constants
from gator import files
from gator import util

WHITESPACE_RE = r"[!\"#$%&()*+,\./:;\<=\>\?\@\[\]\^`\{\|\}]"


def get_paragraphs(contents):
    """Retrieves the paragraphs in the writing in the contents parameter"""
    ast = commonmark.Parser().parse(contents)
    paragraph_content = constants.markers.Nothing
    mode_looking = True
    paragraph_list = []
    counter = 0

    # iterate through the markdown to find paragraphs and add their contents to paragraph_list
    for subnode, enter in ast.walker():
        if mode_looking:
            # check to see if the current subnode is an open paragraph node
            if counter == 1 and subnode.t == constants.markdown.Paragraph and enter:
                # initialize paragraph_content
                paragraph_content = constants.markers.Nothing
                # stop search for paragraph nodes, as one has been found
                # instead, start adding content to paragraph_content
                mode_looking = False
        else:
            # check to see if the current subnode is a closing paragraph node
            if counter == 2 and subnode.t == constants.markdown.Paragraph and not enter:
                # add the content of the paragraph to paragraph_list
                paragraph_list.append(paragraph_content.strip())
                # stop saving paragraph contents, as the paragraph had ended
                # start a search for a new paragraph
                mode_looking = True
            # if the subnode literal has contents,
            # or it is a softbreak, add them to paragraph_content
            if subnode.t == constants.markdown.Softbreak:
                paragraph_content += constants.markers.Newline
            elif subnode.literal is not None:
                paragraph_content += subnode.literal

        # track the how deep into the tree the search currently is
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
    if (
        line is not None
        and line is not constants.markers.Nothing
        and not line.isspace()
    ):
        return False
    return True


def count_paragraphs(contents):
    """Counts the number of paragraphs in the writing"""
    matching_paragraphs = get_paragraphs(contents)
    return len(matching_paragraphs)


def count_words(contents):
    """Counts the minimum number of words across all paragraphs in writing"""
    # retrieve all of the paragraphs in the contents
    # NOTE: this causes word counting to only be supported for markdown!
    paragraphs = get_paragraphs(contents)
    # count all of the words in each paragraph
    word_counts = []
    for para in paragraphs:
        # split the string by whitespace (e.g., newlines or spaces) and punctuation
        words = re.sub(WHITESPACE_RE, constants.markers.Space, para).split()
        word_counts.append(len(words))
    # return the minimum number of words across all paragraphs
    if word_counts:
        return min(word_counts)
    # counting did not work correctly (probably because there were
    # no paragraphs), so return 0 to indicate that no words were found
    return 0


def count_total_words(contents):
    """Counts the total number of words in writing"""
    # retrieve all of the paragraphs in the contents
    # NOTE: this causes word counting to only be supported for markdown!
    paragraphs = get_paragraphs(contents)
    # count all of the words in each paragraph
    word_counts = []
    for para in paragraphs:
        # split the string by whitespace (e.g., newlines or spaces) and punctuation
        words = re.sub(r"[!\"#$%&()*+,\./:;\<=\>\?\@\[\]\^`\{\|\}]", " ", para).split()
        word_counts.append(len(words))
    if word_counts:
        return sum(word_counts)
    # counting did not work correctly (probably because there were
    # no paragraphs), so return 0
    return 0


def count_specified_fragment(contents, fragment):
    """Counts the specified string fragment in the string contents"""
    fragment_count = contents.count(fragment)
    return fragment_count


def count_specified_regex(contents, regex):
    """Counts all the specified regex for a given file"""
    # not a valid regular expression, so return an valid response
    if not is_valid_regex(regex):
        return constants.markers.Invalid
    # the regular expression was valid, return the number of matches
    matches = re.findall(regex, contents, re.DOTALL)
    return len(matches)


# pylint: disable=bad-continuation
def specified_entity_greater_than_count(
    chosen_fragment,
    checking_function,
    expected_count,
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
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
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
):
    """Counts fragments for the file in the directory (or contents) and a fragment"""
    # create a Path object to the chosen file in the containing directory
    file_for_checking = files.create_path(file=given_file, home=containing_directory)
    file_contents_count = 0
    # file is not available and the contents are provided
    # the context for this condition is when the function checks
    # the output from the execution of a specified command
    if not file_for_checking.is_file() and contents is not constants.markers.Nothing:
        file_contents_count = checking_function(contents, chosen_fragment)
    # file is available and the contents are not provided
    # the context for this condition is when the function checks
    # the contents of a specified file
    elif file_for_checking.is_file() and contents is constants.markers.Nothing:
        # read the text from the file and the check for the chosen fragment
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents, chosen_fragment)
    return file_contents_count


# pylint: disable=bad-continuation
def specified_source_greater_than_count(
    expected_count,
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Determines if the line count is greater than expected"""
    # count the fragments in either a file in a directory or String contents
    file_line_count = count_lines(given_file, containing_directory, contents)
    # the fragment count is at or above the threshold
    # check the condition and also return file_fragment_count
    return util.greater_than_equal_exacted(file_line_count, expected_count, exact)


def count_lines(
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
):
    """Counts lines for the file in the directory (or contents)"""
    # create a Path object to the chosen file in the containing directory
    file_for_checking = files.create_path(file=given_file, home=containing_directory)
    file_contents_count = 0
    # file is not available and the contents are provided
    # the context for this condition is when the function checks
    # the output from the execution of a specified command
    if not file_for_checking.is_file() and contents is not constants.markers.Nothing:
        line_list = get_line_list(contents)
        file_contents_count = len(line_list)
    # file is available and the contents are not provided
    # the context for this condition is when the function checks
    # the contents of a specified file
    elif file_for_checking.is_file() and contents is constants.markers.Nothing:
        file_contents = file_for_checking.read_text()
        line_list = get_line_list(file_contents)
        file_contents_count = len(line_list)
    return file_contents_count


def is_valid_regex(regex):
    """Determines if the provided regex is valid"""
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
