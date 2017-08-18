""" Invokes programs on the command-line on behalf of GatorGrader """

import os
import pytest

import gatorgrader
import gatorgrader_files

COURSES = "courses"
ALL = "all"
SEPARATOR = "/"


def invoke_all_file_in_directory_checks(files, directories):
    """ Repeatedly run function that runs pytest """
    # gatorgrader_home, had_to_set_gatorgrader_home = gatorgrader.get_gatorgrader_home()
    # os.environ["GATORGRADER_HOME"] = gatorgrader_home
    # os.chdir(gatorgrader_home + COURSES + SEPARATOR + ALL)
    for filecheck, directory in zip(files, directories):
        invoke_file_in_directory(filecheck, directory)


def invoke_file_in_directory(filecheck, directory):
    """ Runs pytest to check if the file is in a directory """
    gatorgrader_home, had_to_set_gatorgrader_home = gatorgrader.get_gatorgrader_home(
    )
    print("gg home", gatorgrader_home)
    print("had to set?", had_to_set_gatorgrader_home)
    was_file_found = gatorgrader_files.check_file_in_directory(
        filecheck, gatorgrader_home + directory)
    print("found?", was_file_found)
    # assert was_file_found is True

    # print("getting read to call pytest!")
    # gatorgrader_home, had_to_set_gatorgrader_home = gatorgrader.get_gatorgrader_home()
    # print("grtpytest gg home", gatorgrader_home)
    # print("grtpytest had to set", had_to_set_gatorgrader_home)
    # pytest.main([
    # '-s', '--runfiles', '--directory', directory, '--checkfile', filecheck
    # ])
