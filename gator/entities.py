"""Count entities with provided functions."""

from gator import constants
from gator import files
from gator import util


def entity_greater_than_count_total(
    given_file, containing_directory, expected_count, checking_function, exact=False
):
    """Return a count and determination if entity count is greater than expected."""
    # call the count_entities function in this module
    file_entity_count, file_entity_count_dictionary = count_entities(
        given_file, containing_directory, checking_function
    )
    count_status_list = util.greater_than_equal_exacted(
        expected_count, file_entity_count, exact
    )
    count_status = count_status_list[0]
    return count_status, file_entity_count, file_entity_count_dictionary


def entity_greater_than_count(
    given_file, containing_directory, expected_count, checking_function, exact=False
):
    """Return a count and determination if entity count is greater than expected."""
    # call the count_entities function in this module
    file_entity_count, file_entity_count_dictionary = count_entities(
        given_file, containing_directory, checking_function
    )
    final_check_result_list = util.greater_than_equal_exacted(
        file_entity_count, expected_count, exact
    )
    final_check_result = final_check_result_list[0]
    return final_check_result, file_entity_count, file_entity_count_dictionary


def count_entities(given_file, containing_directory, checking_function):
    """Count the number of entities for the file(s) in the directory."""
    # create an empty dictionary of filenames and an internal dictionary
    file_counts_dictionary = {}
    # if the file is not found in the directory, the count is zero
    file_contents_count = 0
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
        # extract the text from the file_for_checking
        file_contents = file_for_checking.read_text()
        # use the provided checking_function to check the contents of the file
        # note this works since Python supports passing a function to a function
        file_contents_count, file_contents_count_dictionary = checking_function(
            file_contents
        )
        # the checking_function returned a dictionary of form {entity: count}
        # so we should store this dictionary insider the containing dictionary
        # this case would occur for checks like number of words in paragraphs
        if file_contents_count_dictionary:
            # associate these file counts with the filename in a dictionary
            file_counts_dictionary[
                file_for_checking.name
            ] = file_contents_count_dictionary
        # the checking_function did not return a dictionary because that was
        # not sensible for the type of check (e.g., counting paragraphs)
        # so we should make a "dummy" dictionary containing the entity count
        else:
            file_contents_count_dictionary = {1: file_contents_count}
            file_counts_dictionary[
                file_for_checking.name
            ] = file_contents_count_dictionary
    # find the minimum count for all paragraphs across all of the files
    # assume that nothing was found and the count is zero and prove otherwise
    file_contents_count_overall = file_contents_count
    # there is a dictionary of counts for files, so deeply find the minimum
    # as long as the count is not of the total words in a file
    if (
        file_counts_dictionary
        and checking_function.__name__ != constants.functions.Count_Total_Words
    ):
        file_contents_count_overall = util.get_first_minimum_value_deep(
            file_counts_dictionary
        )[1][1]
    # return the overall requested count and the nested file count dictionary
    return file_contents_count_overall, file_counts_dictionary
