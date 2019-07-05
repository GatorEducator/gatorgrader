"""Count entities with provided functions."""

from gator import util
from gator import files


# pylint: disable=bad-continuation
def entity_greater_than_count(
    given_file, containing_directory, expected_count, checking_function, exact=False
):
    """Return a count and determination if entity count is greater than expected."""
    # call the count_entities function in this module
    file_entity_count, file_entity_count_dictionary = count_entities(
        given_file, containing_directory, checking_function
    )
    # check the condition and also return file_entity_count
    condition_result, value = util.greater_than_equal_exacted(
        file_entity_count, expected_count, exact
    )
    return condition_result, value, file_entity_count_dictionary


def count_entities(given_file, containing_directory, checking_function):
    """Count the number of entities for the file(s) in the directory."""
    # create an empty dictionary of filenames and an internal dictionary
    file_counts_dictionary = {}
    # create a path for the given file and its containing directory
    # note that this call does not specify any *args and thus there
    # are no directories between the home directory and the file
    for file_for_checking in files.create_paths(
        file=given_file, home=containing_directory
    ):
        # start the count of the number of entities at zero, assuming none found yet
        file_contents_count = 0
        # create an empty dictionary of the counts
        file_contents_count_dictionary = {}
        # a valid file exists and thus it is acceptable to perform the checking
        if file_for_checking.is_file():
            # extract the text from the file_for_checking
            file_contents = file_for_checking.read_text()
            # use the provided checking_function to check the contents of the file
            # note this works since Python supports passing a function to a function
            file_contents_count, file_contents_count_dictionary = checking_function(
                file_contents
            )
            file_counts_dictionary[
                file_for_checking.name
            ] = file_contents_count_dictionary
    file_contents_count_overall = util.get_first_minimum_value_deep(
        file_counts_dictionary
    )[1][1]
    return file_contents_count_overall, file_counts_dictionary
