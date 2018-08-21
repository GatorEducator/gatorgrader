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
PYTHON = "Python"

NOTHING = ""
NO_DIAGNOSTIC = ""
SPACE = " "

MULTIPLE = "multiple-line"
SINGLE = "single-line"


def invoke_commits_check(student_repository, expected_count):
    """Check to see if the repository has more than specified commits"""
    did_check_pass, actual_count = repository.commits_greater_than_count(
        student_repository, expected_count
    )
    # create the message and the diagnostic
    message = "Repository has at least " + str(expected_count) + " commit(s)"
    diagnostic = "Found " + str(actual_count) + " commit(s) in the Git repository"
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


def update_report(status, message, diagnostic):
    """Update the report after running a check"""
    # found at least the required number of an entity
    # do not produce a diagnostic message
    if status:
        report.add_result(message, status, NO_DIAGNOSTIC)
    # did not find at least the required number of an entity
    # produce a diagnostic message using the actual count
    else:
        report.add_result(message, status, diagnostic)


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
        + " comment(s)"
    )
    diagnostic = "Found " + str(actual_count) + " comment(s) in the specified file"
    update_report(met_or_exceeded_count, message, diagnostic)
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
        + "paragraph(s)"
    )
    diagnostic = "Found " + str(actual_count) + " paragraph(s) in the specified file"
    update_report(met_or_exceeded_count, message, diagnostic)
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
        + "word(s) in every paragraph"
    )
    diagnostic = (
        "Found " + str(actual_count) + " word(s) in a paragraph of the specified file"
    )
    update_report(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_fragment_checks(
    fragment, expected_count, filecheck=NOTHING, directory=NOTHING, contents=NOTHING
):
    """Perform the check for a fragment existence in file or contents and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_fragment_greater_than_count(
        fragment,
        fragments.count_specified_fragment,
        expected_count,
        filecheck,
        directory,
        contents,
    )
    # create a message for a file in directory
    if contents is NOTHING:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has at least "
            + str(expected_count)
            + " of the '"
            + fragment
            + "' fragment"
        )
    # create a message for a string
    else:
        message = (
            "The output"
            + " has at least "
            + str(expected_count)
            + " of the '"
            + fragment
            + "' fragment"
        )
    diagnostic = (
        "Found "
        + str(actual_count)
        + " fragment(s) in the output or the specified file"
    )
    update_report(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_command_fragment_checks(command, expected_fragment, expected_count):
    """Perform the check for a fragment existence in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_fragment_checks(
        expected_fragment, expected_count, contents=command_output
    )


def invoke_all_command_checks(command, expected_count):
    """Repeatedly perform the command check and return the results"""
    was_exactly_equal_list = []
    was_exactly_count = 0
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
    return was_exactly_equal_list
