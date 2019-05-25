"""Count entities with provided functions"""

from gator import util
from gator import files


# pylint: disable=bad-continuation
def entity_greater_than_count(
    given_file, containing_directory, expected_count, checking_function, exact=False
):
    """Return count and determines if the entity count is greater than expected"""
    # call the count_entities function in this module
    file_entity_count = count_entities(
        given_file, containing_directory, checking_function
    )
    # check the condition and also return file_entity_count
    return util.greater_than_equal_exacted(file_entity_count, expected_count, exact)


def count_entities(given_file, containing_directory, checking_function):
    """Counts the number of entities for the file in the directory"""
    # create a path for the given file and its containing directory
    # note that this call does not specify any *args and thus there
    # are no directories between the home directory and the file
    file_for_checking = files.create_path(file=given_file, home=containing_directory)
    file_contents_count = 0
    if file_for_checking.is_file():
        file_contents = file_for_checking.read_text()
        file_contents_count = checking_function(file_contents)
    return file_contents_count
