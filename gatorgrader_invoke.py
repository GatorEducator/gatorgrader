""" Invokes programs on the command-line on behalf of GatorGrader """

import os
import pytest

COURSES = "courses"
ALL = "all"
SEPARATOR = "/"


def invoke_all_file_in_directory_checks(files, directories):
    """ Repeatedly run function that runs pytest """
    os.chdir(COURSES + SEPARATOR + ALL)
    for filecheck, directory in zip(files, directories):
        invoke_file_in_directory(filecheck, directory)


def invoke_file_in_directory(filecheck, directory):
    """ Runs pytest to check if the file is in a directory """
    pytest.main([
        '--runfiles', '--directory', directory, '--checkfile', filecheck
    ])
