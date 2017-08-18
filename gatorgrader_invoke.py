""" Invokes programs on the command-line on behalf of GatorGrader """

import gatorgrader
import gatorgrader_files
import gatorgrader_util


def invoke_all_file_in_directory_checks(files, directories):
    """ Repeatedly perform the check and return the results """
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
    """ Check to see if the file is in the directory """
    gatorgrader_home, had_to_set_gatorgrader_home = gatorgrader.get_gatorgrader_home(
    )
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
