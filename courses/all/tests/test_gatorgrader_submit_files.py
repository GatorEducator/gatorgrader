""" GatorGrader tests for files """

import os
import pytest

import gatorgrader_files

CWD = "."

files = pytest.mark.skipif(
    not pytest.config.getoption("--runfiles"),
    reason="needs the --runfiles option to run")


@files
def test_file_exists_in_directory(checkfile, directory):
    """ Check that the file exists in the directory """
    print("file", checkfile)
    print("directory", directory)
    # if directory == CWD:
        # directory = os.path.basename(os.getcwd()) + ".." + "/" + ".." + "/"
    was_file_found = gatorgrader_files.check_file_in_directory(checkfile, directory)
    assert was_file_found is True
