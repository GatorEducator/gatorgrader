"""Test cases for the invoke module"""

import sys

import pytest

from gator import invoke
from gator import report


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary"""
    report.reset()


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_commit_checks(reset_results_dictionary):
    """Checks to that invocation of commit check works correctly"""
    invoke.invoke_commits_check(".", sys.maxsize)
    details = report.get_details()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check(reset_results_dictionary, tmpdir):
    """Checks to that invocation of file existence check works correctly"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    hello_file = "hello.txt"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_details()
    assert details is not None
