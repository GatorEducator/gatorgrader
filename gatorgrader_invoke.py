""" Invokes programs on the command-line on behalf of GatorGrader """

import gatorgrader
import gatorgrader_comments
import gatorgrader_entities
import gatorgrader_files
import gatorgrader_fragments
import gatorgrader_repository
import gatorgrader_run
import gatorgrader_util

JAVA = "Java"
MULTIPLE = "multiple-line"
PYTHON = "Python"
SINGLE = "single-line"


def invoke_commits_check(repository, expected_count):
    """Check to see if the repository has more than specified commits"""
    print("Checking for commits...")
    print()
    did_check_pass =\
        gatorgrader_repository.\
        commits_greater_than_count(repository, expected_count)
    print(
        "Did the repository have at least ",
        expected_count,
        " commits? ",
        gatorgrader_util.get_human_answer(did_check_pass),
        sep="")
    print()
    print("... Done checking for commits")
    return did_check_pass


def invoke_all_file_in_directory_checks(files, directories):
    """Repeatedly perform the check and return the results"""
    print("Checking if files are in the expected directories ...")
    print()
    was_file_found_list = []
    for filecheck, directory in zip(files, directories):
        was_file_found = invoke_file_in_directory_check(filecheck, directory)
        was_file_found_list.append(was_file_found)
    print()
    print("... Done checking if files are in the expected directories")
    return was_file_found_list


def invoke_file_in_directory_check(filecheck, directory):
    """Check to see if the file is in the directory"""
    gatorgrader_home, had_to_set_gatorgrader_home =\
        gatorgrader.get_gatorgrader_home()
    was_file_found = gatorgrader_files.check_file_in_directory(
        filecheck, gatorgrader_home + directory)
    print(
        "Was ",
        filecheck,
        " found in ",
        directory,
        "? ",
        gatorgrader_util.get_human_answer(was_file_found),
        sep="")
    return was_file_found


def invoke_all_comment_checks(files, directories, expected_counts,
                              comment_type, languages):
    """Repeatedly perform the check and return the results"""
    print("Checking for", comment_type, "comments...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    for filecheck, directory, expected_count, language in zip(
            files, directories, expected_counts, languages):
        if comment_type == SINGLE:
            if language == JAVA:
                met_or_exceeded_count =\
                        gatorgrader_entities.entity_greater_than_count(
                            filecheck, directory, expected_count,
                            gatorgrader_comments.count_singleline_java_comment)
            if language == PYTHON:
                met_or_exceeded_count =\
                    gatorgrader_entities.entity_greater_than_count(
                        filecheck, directory, expected_count,
                        gatorgrader_comments.count_singleline_python_comment)
        elif comment_type == MULTIPLE:
            met_or_exceeded_count =\
                gatorgrader_entities.entity_greater_than_count(
                    filecheck, directory, expected_count,
                    gatorgrader_comments.count_multiline_java_comment)

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
            gatorgrader_util.get_human_answer(met_or_exceeded_count),
            sep="")

    print()
    print("... Done checking for", comment_type, "comments")
    return was_exceeded_list


def invoke_all_paragraph_checks(files, directories, expected_counts):
    """Repeatedly perform the check and return the results"""
    print("Checking for paragraphs...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    for filecheck, directory, expected_count in zip(files, directories,
                                                    expected_counts):
        met_or_exceeded_count = gatorgrader_entities.entity_greater_than_count(
            filecheck, directory, expected_count,
            gatorgrader_fragments.count_paragraphs)

        was_exceeded_list.append(met_or_exceeded_count)
        print(
            "Did ",
            filecheck,
            " in ",
            directory,
            " have at least ",
            expected_count,
            " paragraph(s)? ",
            gatorgrader_util.get_human_answer(met_or_exceeded_count),
            sep="")

    print()
    print("... Done checking for paragraphs")
    return was_exceeded_list


def invoke_all_sentence_checks(files, directories, expected_counts):
    """Repeatedly perform the check and return the results"""
    print("Checking for sentences...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    for filecheck, directory, expected_count in zip(files, directories,
                                                    expected_counts):
        met_or_exceeded_count = gatorgrader_entities.entity_greater_than_count(
            filecheck, directory, expected_count,
            gatorgrader_fragments.count_sentences)

        was_exceeded_list.append(met_or_exceeded_count)
        print(
            "Did ",
            filecheck,
            " in ",
            directory,
            " have paragraphs with at least ",
            expected_count,
            " sentence(s)? ",
            gatorgrader_util.get_human_answer(met_or_exceeded_count),
            sep="")

    print()
    print("... Done checking for sentences")
    return was_exceeded_list


def invoke_all_fragment_checks(files, directories, fragments, expected_counts):
    """Repeatedly perform the check and return the results"""
    print("Checking for fragments...")
    print()
    was_exceeded_list = []
    met_or_exceeded_count = 0
    for filecheck, directory, fragment, expected_count in zip(
            files, directories, fragments, expected_counts):
        met_or_exceeded_count =\
            gatorgrader_fragments.specified_fragment_greater_than_count(
                filecheck, directory, fragment, expected_count,
                gatorgrader_fragments.count_specified_fragment)

        was_exceeded_list.append(met_or_exceeded_count)
        print(
            "Did ",
            filecheck,
            " in ",
            directory,
            " have at least ",
            expected_count,
            " of the \"",
            fragment,
            "\" fragment? ",
            gatorgrader_util.get_human_answer(met_or_exceeded_count),
            sep="")

    print()
    print("... Done checking for fragments")
    return was_exceeded_list


def invoke_all_command_checks(commands, expected_counts):
    """Repeatedly perform the check and return the results"""
    print("Checking the output of commands ...")
    print()
    was_exactly_equal_list = []
    was_exactly_count = 0
    for command, expected_count in zip(commands, expected_counts):
        was_exactly_count =\
            gatorgrader_run.specified_command_output_equals_count(
                command, expected_count)

        was_exactly_equal_list.append(was_exactly_count)
        print(
            "Did the command \'",
            command,
            "\' produce exactly ",
            expected_count,
            " lines of output? ",
            gatorgrader_util.get_human_answer(was_exactly_count),
            sep="")

    print()
    print("... Done checking the output of commands")
    return was_exactly_equal_list


def invoke_all_command_fragment_checks(commands, expected_fragment):
    """Repeatedly perform the check and return the results"""
    print("Checking the output of commands ...")
    print()
    was_contained_list = []
    for command, expected_fragment in zip(
            commands, expected_fragment):
        was_contained =\
            gatorgrader_run.specified_command_output_contains_fragment(
                command, expected_fragment)

        was_contained_list.append(was_contained)
        print(
            "Did the command \'",
            command,
            "\' output the fragment \'",
            expected_fragment,
            "\'? ",
            gatorgrader_util.get_human_answer(was_contained),
            sep="")

    print()
    print("... Done checking the output of commands")
    return was_contained_list
