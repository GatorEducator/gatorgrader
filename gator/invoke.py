"""Invokes programs on the command-line"""

from gator import comments
from gator import constants
from gator import entities
from gator import files
from gator import fragments
from gator import markdown
from gator import report
from gator import repository
from gator import run
from gator import util


MULTIPLE = "multiple-line"
SINGLE = "single-line"

SUCCESS = 0


def report_result(status, message, diagnostic):
    """Set the report after running a check"""
    if status:
        # passed the check, so do not produce a diagnostic message
        report.set_result(message, status, constants.markers.No_Diagnostic)
    else:
        # did not pass the check, so produce a diagnostic message
        report.set_result(message, status, diagnostic)


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
    # diagnostic is created when repository does not have sufficient commits
    # call report_result to update report for this check
    diagnostic = "Found " + str(actual_count) + " commit(s) in the Git repository"
    report_result(did_check_pass, message, diagnostic)
    return did_check_pass


def invoke_file_in_directory_check(filecheck, directory):
    """Check to see if the file is in the directory"""
    # get the home directory for checking and then check for file
    gatorgrader_home = util.get_gatorgrader_home()
    was_file_found = files.check_file_in_directory(
        directory, file=filecheck, home=gatorgrader_home
    )
    # construct the message about whether or not the file exists
    message = (
        "The file " + filecheck + " exists in the " + directory + constants.markers.Space + "directory"
    )
    # diagnostic is created when file does not exist in specified directory
    # call report_result to update report for this check
    diagnostic = (
        "Did not find the specified file in the " + directory + constants.markers.Space + "directory"
    )
    report_result(was_file_found, message, diagnostic)
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
        if language == constants.languages.Java:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_java_comment,
                exact,
            )
        # check comments in Python
        if language == constants.languages.Python:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_python_comment,
                exact,
            )
    # check multiple-line comments
    elif comment_type == MULTIPLE:
        # check comments in Java
        if language == constants.languages.Java:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_multiline_java_comment,
                exact,
            )
        # check comments in Python
        if language == constants.languages.Python:
            met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_multiline_python_comment,
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
            + constants.markers.Space
            + comment_type
            + constants.markers.Space
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
            + constants.markers.Space
            + comment_type
            + constants.markers.Space
            + language
            + " comment(s)"
        )
    diagnostic = "Found " + str(actual_count) + " comment(s) in the specified file"
    report_result(met_or_exceeded_count, message, diagnostic)
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
            + constants.markers.Space
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
            + constants.markers.Space
            + "paragraph(s)"
        )
    diagnostic = "Found " + str(actual_count) + " paragraph(s) in the specified file"
    report_result(met_or_exceeded_count, message, diagnostic)
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
            + constants.markers.Space
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
            + constants.markers.Space
            + "word(s) in every paragraph"
        )
    diagnostic = (
        "Found " + str(actual_count) + " word(s) in a paragraph of the specified file"
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_total_word_count_checks(
    filecheck, directory, expected_count, exact=False
):
    """Perform the word count check and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_total_words
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
            + constants.markers.Space
            + "word(s) in total"
        )
    else:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has exactly "
            + str(expected_count)
            + constants.markers.Space
            + "word(s) in total"
        )
    diagnostic = "Found " + str(actual_count) + " word(s) in the specified file"
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_fragment_checks(
    fragment,
    expected_count,
    filecheck=constants.markers.Nothing,
    directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Perform the check for a fragment existence in file or contents and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_entity_greater_than_count(
        fragment,
        fragments.count_specified_fragment,
        expected_count,
        filecheck,
        directory,
        contents,
        exact,
    )
    # create a message for a file in directory
    if filecheck is not constants.markers.Nothing and directory is not constants.markers.Nothing:
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
                "The command output"
                + " has at least "
                + str(expected_count)
                + " of the '"
                + fragment
                + "' fragment"
            )
        else:
            message = (
                "The command output"
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
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_regex_checks(
    regex,
    expected_count,
    filecheck=constants.markers.Nothing,
    directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Perform the check for a regex existence in file or contents and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_entity_greater_than_count(
        regex,
        fragments.count_specified_regex,
        expected_count,
        filecheck,
        directory,
        contents,
        exact,
    )
    # create a message for a file in directory
    if filecheck is not constants.markers.Nothing and directory is not constants.markers.Nothing:
        if exact is not True:
            message = (
                "The "
                + filecheck
                + " in "
                + directory
                + " has at least "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
        else:
            message = (
                "The "
                + filecheck
                + " in "
                + directory
                + " has exactly "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
    # create a message for a string
    else:
        if exact is not True:
            message = (
                "The command output"
                + " has at least "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
        else:
            message = (
                "The command output"
                + " has exactly "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
    diagnostic = (
        "Found "
        + str(actual_count)
        + " matches of the specified regular expression in the output or the specified file"
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_command_fragment_checks(
    command, expected_fragment, expected_count, exact=False
):
    """Perform the check for a fragment existence in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_fragment_checks(
        expected_fragment, expected_count, constants.markers.Nothing, constants.markers.Nothing, command_output, exact
    )


# pylint: disable=bad-continuation
def invoke_all_command_regex_checks(
    command, expected_regex, expected_count, exact=False
):
    """Perform the check for a regex existence in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_regex_checks(
        expected_regex, expected_count, constants.markers.Nothing, constants.markers.Nothing, command_output, exact
    )


def invoke_all_command_executes_checks(command):
    """Perform the check for whether or not a command runs without error"""
    # pylint: disable=unused-variable
    command_output, command_error, command_returncode = run.run_command(command)
    # note that a zero-code means that the command did not work
    # this is the opposite of what is used for processes
    # but, all other GatorGrader checks return 0 on failure and 1 on success
    command_passed = False
    if command_error == constants.markers.Empty and command_returncode == SUCCESS:
        command_passed = True
    message = "The command '" + str(command) + "'" + " executes correctly"
    diagnostic = "The command returned the error code " + str(command_returncode)
    report_result(command_passed, message, diagnostic)
    return command_passed


# pylint: disable=bad-continuation
def invoke_all_markdown_checks(
    markdown_tag, expected_count, filecheck, directory, exact=False
):
    """Perform the check for a markdown tag existence in a file and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = markdown.specified_tag_greater_than_count(
        markdown_tag,
        markdown.count_specified_tag,
        expected_count,
        filecheck,
        directory,
        exact,
    )
    # create a message for a file in directory
    if exact is not True:
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has at least "
            + str(expected_count)
            + " of the '"
            + markdown_tag
            + "' elements"
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
            + markdown_tag
            + "' elements"
        )
    diagnostic = "Found " + str(actual_count) + " element(s) in the specified file"
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_count_checks(
    expected_count, filecheck=constants.markers.Nothing, directory=constants.markers.Nothing, contents=constants.markers.Nothing, exact=False
):
    """Perform the check for the count of lines in file or contents and return the results"""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_source_greater_than_count(
        expected_count, filecheck, directory, contents, exact
    )
    # create a message for a file in directory
    if filecheck is not constants.markers.Nothing and directory is not constants.markers.Nothing:
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
    # create a message for a string (normally from program execution)
    else:
        if exact is not True:
            message = (
                "The command output" + " has at least " + str(expected_count) + " lines"
            )
        else:
            message = (
                "The command output" + " has exactly " + str(expected_count) + " lines"
            )
    diagnostic = (
        "Found " + str(actual_count) + " line(s) in the output or the specified file"
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_command_count_checks(command, expected_count, exact=False):
    """Perform the check for number of lines in the output of a command"""
    command_output = run.specified_command_get_output(command)
    return invoke_all_count_checks(
        expected_count, constants.markers.Nothing, constants.markers.Nothing, command_output, exact
    )
