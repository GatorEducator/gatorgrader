""" Invokes programs on the command-line on behalf of GatorGrader """

import pytest


def invoke_file_in_directory(filecheck, directory):
    """ Runs pytest to check if the file is in a directory """
