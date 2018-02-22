"""Utility functions that retrieve and count the contents of a file"""

from pathlib import Path
import re
import nltk

FILE_SEPARATOR = "/"

# References:
# https://stackoverflow.com/questions/18568105/how-match-a-paragraph-using-regex
# https://stackoverflow.com/questions/13531204/how-to-match-paragraphs-in-text-with-regx

PARAGRAH_RE = r'(.+?\n\n|.+?$)'
SECTION_MARKER = "#"
CODE_FENCE_MARKER = "```"
GATORGRADER_REPLACEMENT = "GATORGRADER_REPLACEMENT"
NEWLINE = "\n"
DOUBLE_NEWLINE = NEWLINE * 2


def is_paragraph(candidate):
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

    # if nothing has returned by now, the candidate must be a paragraphz
    return True


def get_paragraphs(contents, blank_replace=True):
    """Retrieves the paragraphs in the writing"""
    # use a replacement to handle a string with just spaces
    if blank_replace is True:
        contents = contents.replace(" ", "")
    # replace a single newline with a blank space, respecting double newlines
    contents = contents.replace(DOUBLE_NEWLINE, GATORGRADER_REPLACEMENT)
    contents = contents.replace(NEWLINE, " ")
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


def count_sentences(contents):
    """Counts the number of sentences in the writing"""
    # retrieve all of the paragraphs in the contents
    replace_blank_inputs = False
    paragraphs = get_paragraphs(contents, replace_blank_inputs)
    # count all of the sentences in each paragraph
    sentence_counts = []
    for paragraph in paragraphs:
        paragraph = paragraph.replace("\n", " ")
        sentences = nltk.sent_tokenize(paragraph)
        sentence_counts.append(len(sentences))
    return min(sentence_counts)


def count_specified_fragment(contents, fragment):
    """Counts the specified string fragment in the writing"""
    fragment_count = contents.count(fragment)
    return fragment_count


def specified_fragment_greater_than_count(given_file, containing_directory,
                                          chosen_fragment, expected_count,
                                          checking_function):
    """Determines if the fragment count is greater than expected"""
    file_fragment_count = count_fragments(given_file, containing_directory,
                                          chosen_fragment, checking_function)
    if file_fragment_count >= expected_count:
        return True
    return False


def count_fragments(given_file, containing_directory, chosen_fragment,
                    checking_function):
    """Counts fragments for the file in the directory and a fragment"""
    file_for_checking = Path(containing_directory + FILE_SEPARATOR +
                             given_file)
    file_contents_count = 0
    if file_for_checking.is_file():
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents, chosen_fragment)
    return file_contents_count
