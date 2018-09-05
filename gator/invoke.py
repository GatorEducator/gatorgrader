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

EMPTY = b""
SUCCESS = 0


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


def invoke_commits_check(student_repository, expected_count, exact=False):
    """Check to see if the repository has more than specified commits"""
    # inspect the Git repository internals for the commits
    did_check_pass, actual_count = repository.commits_greater_than_count(
        student_repository, expected_count, exact
    )
    # create the message and the diagnostic
    if not exact:
        message = "Repository has at least " + str(expected_count) + " commit(s)"
    else:
        message = "Repository has exactly " + str(expected_count) + " commit(s)"
    diagnostic = "Found " + str(actual_count) + " commit(s) in the Git repository"
    update_report(did_check_pass, message, diagnostic)
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
    # note that update_report is not called because
    # there will never be a diagnostic for this invoke
    report.add_result(message, was_file_found, NO_DIAGNOSTIC)
    return was_file_found


# pylint: disable=bad-continuation
def invoke_all_comment_checks(
    filecheck, directory, expected_count, comment_type, language, exact=False
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
                exact,
            )
        # check comments in Python
        if language == PYTHON:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_python_comment,
                exact,
            )
    # check multiple-line comments (only in Java)
    elif comment_type == MULTIPLE:
        met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
            filecheck,
            directory,
            expected_count,
            comments.count_multiline_java_comment,
            exact,
        )
    # create the message and the diagnostic
    if not exact:
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
    else:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has exactly "
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


def invoke_all_paragraph_checks(filecheck, directory, expected_count, exact=False):
    """Perform the paragraph check and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_paragraphs, exact
    )
    # create the message and the diagnostic
    if not exact:
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
    else:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has exactly "
            + str(expected_count)
            + SPACE
            + "paragraph(s)"
        )
    diagnostic = "Found " + str(actual_count) + " paragraph(s) in the specified file"
    update_report(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_word_count_checks(filecheck, directory, expected_count, exact=False):
    """Perform the word count check and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_words
    )
    # create the message and the diagnostic
    if not exact:
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
    else:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has exactly "
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
    fragment,
    expected_count,
    filecheck=NOTHING,
    directory=NOTHING,
    contents=NOTHING,
    exact=False,
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
        exact,
    )
    # create a message for a file in directory
    if contents is NOTHING:
        if exact is not True:
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
        else:
            message = (
                "The "
                + filecheck
                + " in "
                + directory
                + " has exactly "
                + str(expected_count)
                + " of the '"
                + fragment
                + "' fragment"
            )
    # create a message for a string
    else:
        if exact is not True:
            message = (
                "The output"
                + " has at least "
                + str(expected_count)
                + " of the '"
                + fragment
                + "' fragment"
            )
        else:
            message = (
                "The output"
                + " has exactly "
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


# pylint: disable=bad-continuation
def invoke_all_command_fragment_checks(
    command, expected_fragment, expected_count, exact=False
):
    """Perform the check for a fragment existence in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_fragment_checks(
        expected_fragment, expected_count, NOTHING, NOTHING, command_output, exact
    )


def invoke_all_command_executes_checks(command):
    """Perform the check for whether or not a command runs without error"""
    command_output, command_error, command_returncode = run.run_command(command)
    command_passed = 0
    if command_error == EMPTY and command_returncode == SUCCESS:
        command_passed = 1
    return command_passed


# pylint: disable=bad-continuation
def invoke_all_count_checks(
    expected_count, filecheck=NOTHING, directory=NOTHING, contents=NOTHING, exact=False
):
    """Perform the check for the count of lines in file or contents and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_source_greater_than_count(
        expected_count, filecheck, directory, contents, exact
    )
    # create a message for a file in directory
    if contents is NOTHING:
        if exact is not True:
            message = (
                "The "
                + filecheck
                + " in "
                + directory
                + " has at least "
                + str(expected_count)
                + " line(s)"
            )
        else:
            message = (
                "The "
                + filecheck
                + " in "
                + directory
                + " has exactly "
                + str(expected_count)
                + " line(s)"
            )
    # create a message for a string
    else:
        if exact is not True:
            message = "The content" + " has at least " + str(expected_count) + " lines"
        else:
            message = "The content" + " has exactly " + str(expected_count) + " lines"
    diagnostic = (
        "Found " + str(actual_count) + " line(s) in the output or the specified file"
    )
    update_report(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_command_count_checks(command, expected_count, exact=False):
    """Perform the check for number of lines in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_count_checks(
        expected_count, NOTHING, NOTHING, command_output, exact
    )
