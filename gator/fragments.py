"""Retrieve and count the contents of a file"""

from pathlib import Path
import re

FILE_SEPARATOR = "/"

# References:
# https://stackoverflow.com/questions/18568105/how-match-a-paragraph-using-regex
# https://stackoverflow.com/questions/13531204/how-to-match-paragraphs-in-text-with-regx

PARAGRAH_RE = r"(.+?\n\n|.+?$)"
SECTION_MARKER = "#"
CODE_FENCE_MARKER = "```"
GATORGRADER_REPLACEMENT = "GATORGRADER_REPLACEMENT"

NEWLINE = "\n"
NOTHING = ""
SPACE = " "
DOUBLE_NEWLINE = NEWLINE * 2


def is_paragraph(candidate):
    """Determines if a writing candidate is a paragraph"""
    # remove whitespace surrounding candidate paragraph
    candidate = candidate.strip()
    # if the paragraph is a markdown header, it is not a paragraph
    if candidate.startswith(SECTION_MARKER):
        return False
    # if the paragraph is a fenced code block, it is not a paragraph
    if candidate.startswith(CODE_FENCE_MARKER):
        return False
    # there may be other edge cases that should be added here in the
    # future -- what other structures look like paragraphs but should
    # not be?
    # if nothing has returned by now, the candidate must be a paragraph
    return True


def get_paragraphs(contents, blank_replace=True):
    """Retrieves the paragraphs in the writing"""
    # use a replacement to handle a string with just spaces
    if blank_replace is True:
        contents = contents.replace(SPACE, NOTHING)
    # replace a single newline with a blank space, respecting double newlines
    contents = contents.replace(DOUBLE_NEWLINE, GATORGRADER_REPLACEMENT)
    contents = contents.replace(NEWLINE, SPACE)
    contents = contents.replace(GATORGRADER_REPLACEMENT, DOUBLE_NEWLINE)
    pattern = re.compile(PARAGRAH_RE)
    paragraphs = pattern.findall(contents)
    # disregard all of the section headers in markdown
    matching_paragraphs = []
    for paragraph in paragraphs:
        if is_paragraph(paragraph) is True:
            matching_paragraphs.append(paragraph)
    return matching_paragraphs


def count_paragraphs(contents):
    """Counts the number of paragraphs in the writing"""
    replace_blank_inputs = True
    matching_paragraphs = get_paragraphs(contents, replace_blank_inputs)
    return len(matching_paragraphs)


def count_words(contents):
    """Counts the minimum number of words across all paragraphs in writing"""
    # retrieve all of the paragraphs in the contents
    replace_blank_inputs = False
    paragraphs = get_paragraphs(contents, replace_blank_inputs)
    # count all of the words in each paragraph
    word_counts = []
    for para in paragraphs:
        para = para.replace(NEWLINE, SPACE)
        words = NOTHING.join(ch if ch.isalnum() else SPACE for ch in para).split()
        word_counts.append(len(words))
    if word_counts:
        return min(word_counts)
    return 0


def count_specified_fragment(contents, fragment):
    """Counts the specified string fragment in the string contents"""
    fragment_count = contents.count(fragment)
    return fragment_count


# pylint: disable=bad-continuation
def specified_fragment_greater_than_count(
    given_file, containing_directory, chosen_fragment, expected_count, checking_function
):
    """Determines if the fragment count is greater than expected"""
    file_fragment_count = count_fragments(
        chosen_fragment, checking_function, given_file, containing_directory
    )
    if file_fragment_count >= expected_count:
        return True, file_fragment_count
    return False, file_fragment_count


# pylint: disable=bad-continuation
def count_fragments(
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
    if not file_for_checking.is_file() and contents is not None:
        file_contents_count = checking_function(contents, chosen_fragment)
    # file is available and the contents are not provided
    elif file_for_checking.is_file() and contents is None:
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents, chosen_fragment)
    return file_contents_count
