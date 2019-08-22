"""Invoke programs on the command-line."""

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

# import snoop
# snoop.install(color="rrt")


def report_result(status, message, diagnostic):
    """Set the report after running a check."""
    if status:
        # passed the check, so do not produce a diagnostic message
        report.set_result(message, status, constants.markers.No_Diagnostic)
    else:
        # did not pass the check, so produce a diagnostic message
        report.set_result(message, status, diagnostic)


def invoke_commits_check(student_repository, expected_count, exact=False):
    """Check to see if the repository has more than specified commits."""
    # inspect the Git repository internals for the commits
    did_check_pass, actual_count = repository.commits_greater_than_count(
        student_repository, expected_count, exact
    )
    # create the message and the diagnostic
    if not exact:
        # create a message for an "at least" because it is not exact
        # the "at least" check is the default, you must opt-in to an exact check
        message = "Repository has at least " + str(expected_count) + " commit(s)"
    else:
        # create a message for an exact check
        message = "Repository has exactly " + str(expected_count) + " commit(s)"
    # diagnostic is created when repository does not have sufficient commits
    # call report_result to update report for this check
    diagnostic = "Found " + str(actual_count) + " commit(s) in the Git repository"
    report_result(did_check_pass, message, diagnostic)
    return did_check_pass


def invoke_file_in_directory_check(filecheck, directory):
    """Check to see if the file is in the directory."""
    # get the project directory for checking and then check for file
    gatorgrader_home = util.get_project_home()
    was_file_found = files.check_file_in_directory(
        directory, file=filecheck, home=gatorgrader_home
    )
    # construct the message about whether or not the file exists
    message = (
        "The file "
        + filecheck
        + " exists in the "
        + directory
        + constants.markers.Space
        + "directory"
    )
    # diagnostic is created when file does not exist in specified directory
    # call report_result to update report for this check
    diagnostic = (
        "Did not find the specified file in the "
        + directory
        + constants.markers.Space
        + "directory"
    )
    report_result(was_file_found, message, diagnostic)
    return was_file_found


# pylint: disable=bad-continuation
def invoke_all_comment_checks(
    filecheck, directory, expected_count, comment_type, language, exact=False
):
    """Perform the comment check and return the results."""
    met_or_exceeded_count = 0
    actual_count = 0
    comment_count_details = {}
    # check single-line comments
    if comment_type == constants.comments.Single_Line:
        # check comments in Java
        if language == constants.languages.Java:
            met_or_exceeded_count, actual_count, comment_count_details = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_java_comment,
                exact,
            )
        # check comments in Python
        if language == constants.languages.Python:
            met_or_exceeded_count, actual_count, comment_count_details = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_python_comment,
                exact,
            )
    # check multiple-line comments
    elif comment_type == constants.comments.Multiple_Line:
        # check comments in Java
        if language == constants.languages.Java:
            met_or_exceeded_count, actual_count, comment_count_details = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_multiline_java_comment,
                exact,
            )
        # check comments in Python
        if language == constants.languages.Python:
            met_or_exceeded_count, actual_count, comment_count_details = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_multiline_python_comment,
                exact,
            )
    # check comments in a not-supported language
    # currently the only valid options are:
    # --> single-line
    # --> multiple-line
    # this means that this check will fail because
    # it will not find any of the specified comments
    else:
        pass
    # create the message and the diagnostic
    if not exact:
        # create an "at least" message, which is the default
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
        # create an "exact" message, which is an opt-in
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
    # create the diagnostic and the report the result
    # produce the diagnostic and report the result
    flat_comment_count_details = util.flatten_dictionary_values(comment_count_details)
    fragment_diagnostic = util.get_file_diagnostic(flat_comment_count_details)
    diagnostic = (
        "Found "
        + str(actual_count)
        + constants.markers.Space
        + "comment(s)"
        + constants.markers.Space
        + fragment_diagnostic
        + constants.markers.Space
        + "or the output"
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    # report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_paragraph_checks(filecheck, directory, expected_count, exact=False):
    """Perform the paragraph check and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count, actual_count_dictionary = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_paragraphs, exact
    )
    # create the message and the diagnostic
    if not exact:
        # create an "at least" message, which is the default
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
        # create an "exact" message, which is an opt-in
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
    # produce the diagnostic and report the result
    flat_actual_count_dictionary = util.flatten_dictionary_values(
        actual_count_dictionary
    )
    fragment_diagnostic = util.get_file_diagnostic(flat_actual_count_dictionary)
    diagnostic = (
        "Found "
        + str(actual_count)
        + constants.markers.Space
        + "paragraph(s)"
        + constants.markers.Space
        + fragment_diagnostic
        + constants.markers.Space
        + constants.markers.File
    )
    # create the diagnostic and then report the result
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_word_count_checks(
    filecheck, directory, expected_count, count_function, conclusion, exact=False
):
    """Perform the word count check and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count, actual_count_dictionary = entities.entity_greater_than_count(
        filecheck, directory, expected_count, count_function
    )
    # create the message and the diagnostic
    # note that the conclusion variable is customized so that it
    # displays the correct message and diagnostic based on whether
    # the check was for a "total words" or a "minimum words" check
    if not exact:
        # create an "at least" message, which is the default
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has at least "
            + str(expected_count)
            + constants.markers.Space
            + conclusion
        )
    else:
        # create an "exact" message, which is an opt-in
        message = (
            "The "
            + filecheck
            + " in "
            + directory
            + " has exactly "
            + str(expected_count)
            + constants.markers.Space
            + conclusion
        )
    # Create a diagnostic message and report the result
    # replace "in every" with "in a" and a specific paragraph number.
    # This diagnostic signals the fact that there was at least
    # a single paragraph that had a word count below the standard
    # set for all of the paragraphs in the technical writing
    # across all of the files specified (i.e., those matched by wildcards)
    word_diagnostic, filename = util.get_word_diagnostic(actual_count_dictionary)
    # there is no need for a filename diagnostic unless there are multiple results
    filename_diagnostic = constants.markers.Nothing
    # there is a filename, which means that there was a wildcard specified
    # and thus this diagnostic is for one file; give name at the end
    if filename:
        filename_diagnostic = (
            constants.markers.Of_File + constants.markers.Space + filename
        )
    # since there is a word_diagnostic, add it to the conclusion of diagnostic
    # otherwise, the conclusion will always contain "in every"
    if word_diagnostic:
        conclusion = conclusion.replace(constants.words.In_Every, word_diagnostic)
    diagnostic = (
        "Found "
        + str(actual_count)
        + constants.markers.Space
        + conclusion
        + constants.markers.Space
        + filename_diagnostic
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


def invoke_all_minimum_word_count_checks(
    filecheck, directory, expected_count, exact=False
):
    """Perform the minimum word count check and return the results."""
    return invoke_all_word_count_checks(
        filecheck,
        directory,
        expected_count,
        fragments.count_minimum_words,
        constants.words.Minimum,
        exact,
    )


def invoke_all_total_word_count_checks(
    filecheck, directory, expected_count, exact=False
):
    """Perform the total word count check and return the results."""
    return invoke_all_word_count_checks(
        filecheck,
        directory,
        expected_count,
        fragments.count_total_words,
        constants.words.Total,
        exact,
    )


# pylint: disable=bad-continuation
def invoke_all_fragment_checks(
    fragment,
    expected_count,
    filecheck=constants.markers.Nothing,
    directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Perform the check for a fragment existence in file or contents and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count, actual_count_dictionary = fragments.specified_entity_greater_than_count(
        fragment,
        fragments.count_specified_fragment,
        expected_count,
        filecheck,
        directory,
        contents,
        exact,
    )
    # create a message for a file in directory
    if (
        filecheck is not constants.markers.Nothing
        and directory is not constants.markers.Nothing
    ):
        # create an "at least" message, which is the default
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
        # create an "exact" message, which is an opt-in
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
    # this case is run when a program is
    # executed and then produces output
    else:
        # create an "at least" message, which is the default
        if exact is not True:
            message = (
                "The command output"
                + " has at least "
                + str(expected_count)
                + " of the '"
                + fragment
                + "' fragment"
            )
        # create an "exact" message, which is an opt-in
        else:
            message = (
                "The command output"
                + " has exactly "
                + str(expected_count)
                + " of the '"
                + fragment
                + "' fragment"
            )
    # produce the diagnostic and report the result
    fragment_diagnostic = util.get_file_diagnostic(actual_count_dictionary)
    diagnostic = (
        "Found "
        + str(actual_count)
        + constants.markers.Space
        + "fragment(s)"
        + constants.markers.Space
        + fragment_diagnostic
        + constants.markers.Space
        + "or the output"
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
    """Perform the check for a regex existence in file or contents and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count, actual_count_dictionary = fragments.specified_entity_greater_than_count(
        regex,
        fragments.count_specified_regex,
        expected_count,
        filecheck,
        directory,
        contents,
        exact,
    )
    # create a message for a file in directory
    if (
        filecheck is not constants.markers.Nothing
        and directory is not constants.markers.Nothing
    ):
        # create an "at least" message, which is the default
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
        # create an "exact" message, which is an opt-in
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
    # this case is run when a program is
    # executed and then produces output
    else:
        # create an "at least" message, which is the default
        if exact is not True:
            message = (
                "The command output"
                + " has at least "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
        # create an "exact" message, which is opt-in
        else:
            message = (
                "The command output"
                + " has exactly "
                + str(expected_count)
                + " matches of the '"
                + regex
                + "' regular expression"
            )
    # only construct a diagnostic for a file if needed
    conclusion = ""
    # use the default name of the file
    violating_file_name = filecheck
    # since a wildcard was specified, pick the file that most violates the check
    if actual_count_dictionary and filecheck is not constants.markers.Nothing:
        violating_entity_details = util.get_first_value(actual_count_dictionary)
        violating_file_name = violating_entity_details[0]
    # create a conclusion to tag onto the diagnostic's ending
    if filecheck is not constants.markers.Nothing:
        conclusion = "or " + violating_file_name
    # create the diagnostic message and report the result
    diagnostic = (
        "Found "
        + str(actual_count)
        + constants.markers.Space
        + "match(es) of the regular expression in output"
        + constants.markers.Space
        + conclusion
    )
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_command_fragment_checks(
    command, expected_fragment, expected_count, exact=False
):
    """Perform the check for a fragment existence in the output of a command."""
    command_output = run.specified_command_get_output(command)
    # Since the command did not produce any output (i.e., its output is "" or
    # Nothing), we need to indicate that this was a command error. This will
    # later signal that, since this command error-ed, the tool should convert
    # the output to "" (i.e., Nothing) instead of looking for a file in a directory.
    # The tool needs this conditional logic since the checking of fragments is
    # overloaded for files in directories and the output of commands.
    if command_output is constants.markers.Nothing:
        command_output = constants.markers.Command_Error
    return invoke_all_fragment_checks(
        expected_fragment,
        expected_count,
        constants.markers.Nothing,
        constants.markers.Nothing,
        command_output,
        exact,
    )


# pylint: disable=bad-continuation
def invoke_all_command_regex_checks(
    command, expected_regex, expected_count, exact=False
):
    """Perform the check for a regex existence in the output of a command."""
    command_output = run.specified_command_get_output(command)
    return invoke_all_regex_checks(
        expected_regex,
        expected_count,
        constants.markers.Nothing,
        constants.markers.Nothing,
        command_output,
        exact,
    )


def invoke_all_command_executes_checks(command):
    """Perform the check for whether or not a command runs without error."""
    # pylint: disable=unused-variable
    # note that the program does not use all of these
    # return values, but we are capturing them if needed for debugging
    command_output, command_error, command_returncode = run.run_command(command)
    # note that a zero-code means that the command did not work
    # this is the opposite of what is used for processes
    # but, all other GatorGrader checks return 0 on failure and 1 on success
    command_passed = False
    if (
        command_error == constants.markers.Empty
        and command_returncode == constants.codes.Success
    ):
        command_passed = True
    # create the message and diagnostic and report the result
    message = "The command '" + str(command) + "'" + " executes correctly"
    diagnostic = "The command returned the error code " + str(command_returncode)
    report_result(command_passed, message, diagnostic)
    return command_passed


# pylint: disable=bad-continuation
def invoke_all_markdown_checks(
    markdown_tag, expected_count, filecheck, directory, exact=False
):
    """Perform the check for a markdown tag existence in a file and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = markdown.specified_tag_greater_than_count(
        markdown_tag,
        markdown.count_specified_tag,
        expected_count,
        filecheck,
        directory,
        exact,
    )
    # create an "at least" message which is the default
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
    # create an "exact" message which is an opt-in
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
    # create the diagnostic and report the result
    diagnostic = "Found " + str(actual_count) + " element(s) in the specified file"
    report_result(met_or_exceeded_count, message, diagnostic)
    return met_or_exceeded_count


# pylint: disable=bad-continuation
def invoke_all_count_checks(
    expected_count,
    filecheck=constants.markers.Nothing,
    directory=constants.markers.Nothing,
    contents=constants.markers.Nothing,
    exact=False,
):
    """Perform the check for the count of lines in file or contents and return the results."""
    met_or_exceeded_count = 0
    met_or_exceeded_count, actual_count = fragments.specified_source_greater_than_count(
        expected_count, filecheck, directory, contents, exact
    )
    # create a message for a file in directory
    if (
        filecheck is not constants.markers.Nothing
        and directory is not constants.markers.Nothing
    ):
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
    """Perform the check for number of lines in the output of a command."""
    command_output = run.specified_command_get_output(command)
    return invoke_all_count_checks(
        expected_count,
        constants.markers.Nothing,
        constants.markers.Nothing,
        command_output,
        exact,
    )
