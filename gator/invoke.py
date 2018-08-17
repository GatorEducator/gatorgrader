"""Invokes programs on the command-line"""

from gator import comments
from gator import entities
from gator import files
from gator import fragments
from gator import report
from gator import repository
from gator import run
from gator import util

JAVA = "Java"
MULTIPLE = "multiple-line"
NO_DIAGNOSTIC = ""
PYTHON = "Python"
SINGLE = "single-line"
SPACE = " "


def invoke_commits_check(student_repository, expected_count):
    """Check to see if the repository has more than specified commits"""
    did_check_pass, actual_count = repository.commits_greater_than_count(
        student_repository, expected_count
    )
    # create the message and the diagnostic
    message = "Repository has at least " + str(expected_count) + " commits"
    diagnostic = "Found " + str(actual_count) + " commits in the Git repository"
    # found at least the required number of commits
    # do not produce a diagnostic message
    if did_check_pass:
        report.add_result(message, did_check_pass, NO_DIAGNOSTIC)
    # did not find at least the required number of commits
    # produce a diagnostic message using the actual count
    else:
        report.add_result(message, did_check_pass, diagnostic)
    return did_check_pass


def invoke_file_in_directory_check(filecheck, directory):
    """Check to see if the file is in the directory"""
    # get the home directory for checking and then check for file
    gatorgrader_home = util.get_gatorgrader_home()
    was_file_found = files.check_file_in_directory(
        filecheck, gatorgrader_home + directory
    )
    # construct the message about whether or not the file exists
    # note that no diagnostic is needed and the result is boolean
    message = (
        "The file " + filecheck + " exists in the " + directory + SPACE + "directory"
    )
    # produce the final report and return the result
    report.add_result(message, was_file_found, NO_DIAGNOSTIC)
    return was_file_found


# pylint: disable=bad-continuation
def invoke_all_comment_checks(
    filecheck, directory, expected_count, comment_type, language
):
    """Perform the comment check and return the results"""
    met_or_exceeded_count = 0
    actual_count = 0
    # check single-line comments
    if comment_type == SINGLE:
        # check comments in Java
        if language == JAVA:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_java_comment,
            )
        # check comments in Python
        if language == PYTHON:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_python_comment,
            )
    # check multiple-line comments (only in Java)
    elif comment_type == MULTIPLE:
        met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
            filecheck, directory, expected_count, comments.count_multiline_java_comment
        )
    message = (
        "The "
        + filecheck
        + " in "
        + directory
        + " has at least "
        + str(expected_count)
        + SPACE
        + comment_type
        + SPACE
        + language
        + " comments"
    )
    diagnostic = "Found " + str(actual_count) + " comments in the specified file"
    # found at least the required number of comments
    # do not produce a diagnostic message
    if met_or_exceeded_count:
        report.add_result(message, met_or_exceeded_count, NO_DIAGNOSTIC)
    # did not find at least the required number of comments
    # produce a diagnostic message using the actual count
    else:
        report.add_result(message, met_or_exceeded_count, diagnostic)
    return met_or_exceeded_count


def invoke_all_paragraph_checks(filecheck, directory, expected_count):
    """Perform the paragraph check and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_paragraphs
    )
    message = (
        "The "
        + filecheck
        + " in "
        + directory
        + " has at least "
        + str(expected_count)
        + SPACE
        + "paragraphs"
    )
    diagnostic = "Found " + str(actual_count) + " paragraphs in the specified file"
    # found at least the required number of paragraphs
    # do not produce a diagnostic message
    if met_or_exceeded_count:
        report.add_result(message, met_or_exceeded_count, NO_DIAGNOSTIC)
    # did not find at least the required number of paragraphs
    # produce a diagnostic message using the actual count
    else:
        report.add_result(message, met_or_exceeded_count, diagnostic)
    return met_or_exceeded_count


def invoke_all_word_count_checks(filecheck, directory, expected_count):
    """Perform the word count check and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_words
    )
    message = (
        "The "
        + filecheck
        + " in "
        + directory
        + " has at least "
        + str(expected_count)
        + SPACE
        + "words"
    )
    diagnostic = "Found " + str(actual_count) + " words in the specified file"
    # found at least the required number of paragraphs
    # do not produce a diagnostic message
    if met_or_exceeded_count:
        report.add_result(message, met_or_exceeded_count, NO_DIAGNOSTIC)
    # did not find at least the required number of words
    # produce a diagnostic message using the actual count
    else:
        report.add_result(message, met_or_exceeded_count, diagnostic)
    return met_or_exceeded_count


def invoke_all_fragment_checks(filecheck, directory, fragment, expected_count):
    """Perform the check for a fragment existence and return the results"""
    print("Checking for fragments...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    met_or_exceeded_count = fragments.specified_fragment_greater_than_count(
        filecheck,
        directory,
        fragment,
        expected_count,
        fragments.count_specified_fragment,
    )
    was_exceeded_list.append(met_or_exceeded_count)
    print(
        "Did ",
        filecheck,
        " in ",
        directory,
        " have at least ",
        expected_count,
        ' of the "',
        fragment,
        '" fragment? ',
        util.get_human_answer(met_or_exceeded_count),
        sep="",
    )

    print()
    print("... Done checking for fragments")
    return was_exceeded_list


def invoke_all_command_checks(command, expected_count):
    """Repeatedly perform the command check and return the results"""
    print("Checking the output of commands ...")
    print()
    was_exactly_equal_list = []
    was_exactly_count = 0
    # for command, expected_count in zip(commands, expected_counts):
    was_exactly_count = run.specified_command_output_equals_count(
        command, expected_count
    )
    was_exactly_equal_list.append(was_exactly_count)
    print(
        "Did the command '",
        command,
        "' produce exactly ",
        expected_count,
        " lines of output? ",
        util.get_human_answer(was_exactly_count),
        sep="",
    )
    print()
    print("... Done checking the output of commands")
    return was_exactly_equal_list


def invoke_all_command_fragment_checks(command, expected_fragment):
    """Repeatedly perform the check and return the results"""
    print("Checking the output of commands ...")
    print()
    was_contained_list = []
    was_contained = run.specified_command_output_contains_fragment(
        command, expected_fragment
    )
    was_contained_list.append(was_contained)
    print(
        "Did the command '",
        command,
        "' output the fragment '",
        expected_fragment,
        "'? ",
        util.get_human_answer(was_contained),
        sep="",
    )
    print()
    print("... Done checking the output of commands")
    return was_contained_list
