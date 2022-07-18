"""Retrieve and count the tags of a markdown file."""

import commonmark

from gator import files
from gator import util


def count_specified_tag(contents, tag):
    """Count the specified markdown tag in the string contents."""
    ast = commonmark.Parser().parse(contents)
    tag_count = 0
    # iteratively check all of the nodes in the AST of the markdown file
    for subnode, enter in ast.walker():
        # check to see if the current subnode is an open node of the specified tag
        if subnode.t == tag and enter:
            tag_count += 1
    return tag_count


def specified_tag_greater_than_count(
    chosen_tag,
    checking_function,
    expected_count,
    given_file,
    containing_directory,
    exact=False,
):
    """Determine if the tag count is greater than expected in given file(s)."""
    # Use these two variables to keep track of tag counts for multiple files.
    # The idea is that file_tags_count_dictionary will store (key, value) pairs
    # where the key is the file and the count is the number of entities in that file.
    file_tags_count = 0
    file_tags_count_dictionary = {}
    # Create a Path object to the chosen file in the containing directory, accounting
    # for the fact that a wildcard like "*.md" will create multiple paths. Note that
    # the create_paths function can only return valid paths, regardless of input.
    for file_for_checking in files.create_paths(
        file=given_file, home=containing_directory
    ):
        file_tag_count = 0
        # since the specified file must be valid and thus suitable for checking,
        # read the contents of the file and then check for the chosen tag
        file_contents = file_for_checking.read_text()
        file_tag_count = checking_function(file_contents, chosen_tag)
        file_tags_count_dictionary[file_for_checking.name] = file_tag_count
    # return the minimum value and the entire dictionary of counts
    minimum_pair = util.get_first_minimum_value(file_tags_count_dictionary)
    file_tags_count = minimum_pair[1]
    # check the condition and also return file_tags_count
    return (
        util.greater_than_equal_exacted(file_tags_count, expected_count, exact),
        file_tags_count_dictionary,
    )
