"""Retrieve and count the contents of a file."""

import re
import commonmark

from gator import constants
from gator import files
from gator import util

# define regular expression for blank space matching
WHITESPACE_RE = r"[!\"#$%&()*+,\./:;\<=\>\?\@\[\]\^`\{\|\}]"


def get_paragraphs(contents):
    """Retrieve the paragraphs in the writing in the contents parameter."""
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
    # return the list of the collected paragraphs
    return paragraph_list


def get_line_list(content):
    """Return a list of lines from any type of input string."""
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
    """Return True if a line is a blank one and False otherwise."""
    if (
        line is not None
        and line is not constants.markers.Nothing
        and not line.isspace()
    ):
        return False
    return True


def count_paragraphs(contents):
    """Count the number of paragraphs in the writing."""
    matching_paragraphs = get_paragraphs(contents)
    # return an empty dictionary because this function is
    # passed as a function to other functions interchangeably
    # with the count_words function which must return two parameters:
    # (1) the count of words and (2) the dictionary of word counts
    return len(matching_paragraphs), {}


def count_words(contents, summarizer=min):
    """Count the total number of words in writing using a summarization function."""
    # create a list for a count of the words in each paragraph
    word_counts = []
    # create a dictionary to map a paragraph number
    # to the count of the number of words in the paragraph
    paragraph_word_counts = {}
    # retrieve all of the paragraphs in the contents
    # word counting only works for technical writing in Markdown
    paragraphs = get_paragraphs(contents)
    # iterate through each paragraph and count its words
    # note that using start=1 means that enumerate will
    # index the first paragraph with the value of 1
    for index, para in enumerate(paragraphs, start=1):
        # for para in paragraphs:
        # split the string by whitespace (e.g., newlines or spaces) and punctuation
        words = re.sub(WHITESPACE_RE, constants.markers.Space, para).split()
        # count the number of words and keep track
        # of the count for this paragraph in the list and dictionary
        word_count = len(words)
        word_counts.append(word_count)
        paragraph_word_counts[index] = word_count
    # word counts exist in the list and thus we can use the provided
    # summarizer (e.g., a sum or a min function) to summarize the count
    if word_counts and paragraph_word_counts:
        return summarizer(word_counts), paragraph_word_counts
    # counting did not work correctly (probably because there were
    # no paragraphs), so return 0 to indicate that there were no words
    return constants.codes.No_Words, paragraph_word_counts


def count_minimum_words(contents):
    """Count the minimum number of words across all paragraphs in writing."""
    # call the count_words function with the min function as a parameter
    return count_words(contents, min)


def count_total_words(contents):
    """Count the total number of words across all paragraphs in writing."""
    # call the count_words function with the sum function as a parameter
    return count_words(contents, sum)


def count_specified_fragment(contents, fragment):
    """Count the specified string fragment in the string contents."""
    fragment_count = contents.count(fragment)
    return fragment_count


def count_specified_regex(contents, regex):
    """Count all the specified regex for a given file."""
    # not a valid regular expression, so return an valid response
    if not is_valid_regex(regex):
        return constants.markers.Invalid
    # the regular expression was valid, return the number of matches
    matches = re.findall(regex, contents, re.DOTALL)
    return len(matches)


def specified_entity_greater_than_count(
    chosen_fragment,
    checking_function,
    expected_count,
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Determine if the entity count is greater than expected."""
    # count the fragments/regex in either a file in a directory or String contents
    file_entity_count, file_entity_count_dictionary = count_entities(
        chosen_fragment, checking_function, given_file, containing_directory, contents
    )
    # check the condition and also return file_entity_count
    condition_truth, value = util.greater_than_equal_exacted(
        file_entity_count, expected_count, exact
    )
    # also return an empty dictionary since this function does not
    # need to count details about multiple entities
    return condition_truth, value, file_entity_count_dictionary


def count_entities(
    chosen_fragment,
    checking_function,
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
):
    """Count fragments for the file in the directory (or contents) and a fragment."""
    # Use these two variables to keep track of entity counts for multiple files.
    # The idea is that file_contents_count_dictionary will store (key, value) pairs
    # where the key is the file and the count is the number of entities in that file.
    file_contents_count = 0
    file_contents_count_dictionary = {}
    # file is not available and the contents are provided
    # the context for this condition is when the function checks
    # the output from the execution of a specified command
    if (
        contents is not constants.markers.Nothing
        and given_file is constants.markers.Nothing
    ):
        # The command ran and produced an error, which means that its output
        # is technically "" or Nothing. So, set it to Nothing so that the
        # checking_function can determine that none of the entity exists in it
        if contents is constants.markers.Command_Error:
            contents = constants.markers.Nothing
        # run the checking_function to look for fragments in the contents
        file_contents_count = checking_function(contents, chosen_fragment)
        return file_contents_count, file_contents_count_dictionary
    for file_for_checking in files.create_paths(
        file=given_file, home=containing_directory
    ):
        # an actual file is available and command contents are not provided
        # the context for this condition is when the function checks file contents
        # read the text from the file and then check for the chosen fragment
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents, chosen_fragment)
        file_contents_count_dictionary[file_for_checking.name] = file_contents_count
    # return the minimum value and the entire dictionary of counts
    minimum_pair = util.get_first_minimum_value(file_contents_count_dictionary)
    file_contents_count = minimum_pair[1]
    return file_contents_count, file_contents_count_dictionary


def specified_source_greater_than_count(
    expected_count,
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Determine if the line count is greater than expected."""
    # count the fragments in either a file in a directory or str contents,
    # with the str contents coming from the output from running a command
    file_lines_count, file_contents_count_dictionary = count_lines(
        given_file, containing_directory, contents
    )
    # the fragment count is at or above the threshold
    # check the condition and also return the file_lines_count
    # and the dictionary itself so as to support good diagnostics
    return (
        (
            util.greater_than_equal_exacted(file_lines_count, expected_count, exact),
            file_lines_count,
        ),
        file_contents_count_dictionary,
    )


def count_lines(
    given_file=constants.markers.Nothing,
    containing_directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
):
    """Count lines for the file in the directory, or alternatively, provided contents."""
    # Use these two variables to keep track of line counts for multiple files.
    # The idea is that file_contents_count_dictionary will store (key, value) pairs
    # where the key is the file and the count is the number of entities in that file.
    file_contents_count = 0
    file_contents_count_dictionary = {}
    # the contents are provided and thus there is no file or directory
    # the context for this condition is when the function checks
    # the output from the execution of a specified command
    if contents is not constants.markers.Nothing:
        line_list = get_line_list(contents)
        file_contents_count = len(line_list)
    # file is and directory are available and thus there are no contents
    # the context for this condition is when the function checks
    # the number of lines in a specific file in a specific directory
    elif (
        given_file is not constants.markers.Nothing
        and containing_directory is not constants.markers.Nothing
    ):
        # Create a Path object to the chosen file in the containing directory, accounting
        # for the fact that a wildcard like "*.md" will create multiple paths. Note that
        # the create_paths function can only return valid paths, regardless of input.
        for file_for_checking in files.create_paths(
            file=given_file, home=containing_directory
        ):
            file_contents_count = 0
            # file is available and the contents are not provided
            # the context for this condition is when the function checks
            # the contents of a specified file that exists on the filesystem
            file_contents = file_for_checking.read_text()
            line_list = get_line_list(file_contents)
            file_contents_count = len(line_list)
            file_contents_count_dictionary[file_for_checking.name] = file_contents_count
        # return the minimum value and the entire dictionary of counts
        minimum_pair = util.get_first_minimum_value(file_contents_count_dictionary)
        file_contents_count = minimum_pair[1]
    return file_contents_count, file_contents_count_dictionary


def is_valid_regex(regex):
    """Determine if the provided regex is valid."""
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
