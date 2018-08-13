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
PYTHON = "Python"
SINGLE = "single-line"


def invoke_commits_check(student_repository, expected_count):
    """Check to see if the repository has more than specified commits"""
    # print("Checking for commits...")
    # print()
    did_check_pass, actual_count = repository.commits_greater_than_count(
        student_repository, expected_count
    )
    
    report.add_result(
        "Did the repository have at least " + str(expected_count) + " commits?",
        util.get_symbol_answer(did_check_pass),
        "",
    )

    # print(
    #     "Did the repository have at least ",
    #     expected_count,
    #     " commits? ",
    #     util.get_human_answer(did_check_pass),
    #     sep="",
    # )

    # print()
    # print("... Done checking for commits")
    return did_check_pass


def invoke_all_file_in_directory_checks(filecheck, directory):
    """Perform the check for file existence and return the results"""
    print("Checking if files are in the expected directories ...")
    print()
    was_file_found_list = []
    was_file_found = invoke_file_in_directory_check(filecheck, directory)
    was_file_found_list.append(was_file_found)
    print()
    print("... Done checking if files are in the expected directories")
    return was_file_found_list


def invoke_file_in_directory_check(filecheck, directory):
    """Check to see if the file is in the directory"""
    gatorgrader_home = util.get_gatorgrader_home()
    was_file_found = files.check_file_in_directory(
        filecheck, gatorgrader_home + directory
    )
    print(
        "Was ",
        filecheck,
        " found in ",
        directory,
        "? ",
        util.get_human_answer(was_file_found),
        sep="",
    )
    return was_file_found


# pylint: disable=bad-continuation
def invoke_all_comment_checks(
    filecheck, directory, expected_count, comment_type, language
):
    """Perform the comment check and return the results"""
    print("Checking for", comment_type, "comments...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    # check single-lie comments
    if comment_type == SINGLE:
        # check comments in Java
        if language == JAVA:
            met_or_exceeded_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_java_comment,
            )
        # check comments in Python
        if language == PYTHON:
            met_or_exceeded_count = entities.entity_greater_than_count(
                filecheck,
                directory,
                expected_count,
                comments.count_singleline_python_comment,
            )
    # check multiple-line comments (only in Java)
    elif comment_type == MULTIPLE:
        met_or_exceeded_count = entities.entity_greater_than_count(
            filecheck, directory, expected_count, comments.count_multiline_java_comment
        )
    was_exceeded_list.append(met_or_exceeded_count)
    print(
        "Did ",
        filecheck,
        " in ",
        directory,
        " have at least ",
        expected_count,
        " ",
        comment_type,
        " comments in the ",
        language,
        " format? ",
        util.get_human_answer(met_or_exceeded_count),
        sep="",
    )

    print()
    print("... Done checking for", comment_type, "comments")
    return was_exceeded_list


def invoke_all_paragraph_checks(filecheck, directory, expected_count):
    """Perform the paragraph check and return the results"""
    print("Checking for paragraphs...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    met_or_exceeded_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_paragraphs
    )
    was_exceeded_list.append(met_or_exceeded_count)
    print(
        "Did ",
        filecheck,
        " in ",
        directory,
        " have at least ",
        expected_count,
        " paragraph(s)? ",
        util.get_human_answer(met_or_exceeded_count),
        sep="",
    )
    print()
    print("... Done checking for paragraphs")
    return was_exceeded_list


def invoke_all_word_count_checks(filecheck, directory, expected_count):
    """Perform the word count check and return the results"""
    print("Checking for word counts...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    met_or_exceeded_count = entities.entity_greater_than_count(
        filecheck, directory, expected_count, fragments.count_words
    )
    was_exceeded_list.append(met_or_exceeded_count)
    print(
        "Did ",
        filecheck,
        " in ",
        directory,
        " have paragraphs with at least ",
        expected_count,
        " words? ",
        util.get_human_answer(met_or_exceeded_count),
        sep="",
    )
    print()
    print("... Done checking for word counts")
    return was_exceeded_list


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
