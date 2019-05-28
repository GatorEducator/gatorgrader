"""Retrieve and count the tags of a markdown file"""

import commonmark

from gator import files
from gator import util


def count_specified_tag(contents, tag):
    """Counts the specified markdown tag in the string contents"""
    ast = commonmark.Parser().parse(contents)
    tag_count = 0

    for subnode, enter in ast.walker():
        # Check to see if the current subnode is an open node of the specified tag
        if subnode.t == tag and enter:
            tag_count += 1

    return tag_count


# pylint: disable=bad-continuation
def specified_tag_greater_than_count(
    chosen_tag,
    checking_function,
    expected_count,
    given_file,
    containing_directory,
    exact=False,
):
    """Determines if the tag count is greater than expected in a given file"""
    # create a Path object to the chosen file in the containing directory
    file_for_checking = files.create_path(file=given_file, home=containing_directory)
    file_tag_count = 0
    # the specified file is a valid done and thus it is suitable for checking
    if file_for_checking.is_file():
        # read the contents of the file and then check for the chosen tag
        file_contents = file_for_checking.read_text()
        file_tag_count = checking_function(file_contents, chosen_tag)

    # check the condition and also return file_tag_count
    return util.greater_than_equal_exacted(file_tag_count, expected_count, exact)
