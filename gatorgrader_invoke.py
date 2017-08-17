""" Invokes programs on the command-line on behalf of GatorGrader """

import os
import pytest

import gatorgrader

COURSES = "courses"
ALL = "all"
SEPARATOR = "/"


def invoke_all_file_in_directory_checks(files, directories):
    """ Repeatedly run function that runs pytest """
    gatorgrader_home, had_to_set_gatorgrader_home = gatorgrader.get_gatorgrader_home()
    os.chdir(gatorgrader_home + COURSES + SEPARATOR + ALL)
    for filecheck, directory in zip(files, directories):
        invoke_file_in_directory(filecheck, directory)


def invoke_file_in_directory(filecheck, directory):
    """ Runs pytest to check if the file is in a directory """
    pytest.main([
        '--runfiles', '--directory', directory, '--checkfile', filecheck
    ])
