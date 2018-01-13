""" test cases for the gatorgrader_files module """

import gatorgrader_files


def test_one_file_found_in_subdirectory(tmpdir):
    """check_file_in_directory can find one file file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = gatorgrader_files.check_file_in_directory(
        "hello.txt", tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is True


def test_many_files_found_in_subdirectory(tmpdir):
    """check_file_in_directory can find many files file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = gatorgrader_files.check_file_in_directory(
        "hello.txt", tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is True
    readme_file = tmpdir.join("sub").join("README.md")
    readme_file.write("# README")
    was_file_found = gatorgrader_files.check_file_in_directory(
        "README.md", tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is True


def test_one_file_not_found_in_subdirectory(tmpdir):
    """check_file_in_directory cannot find one file file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = gatorgrader_files.check_file_in_directory(
        "hello_not_there.txt",
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is False


def test_many_files_not_found_in_subdirectory(tmpdir):
    """check_file_in_directory cannot find many files file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = gatorgrader_files.check_file_in_directory(
        "hello_not_there.txt",
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is False
    readme_file = tmpdir.join("sub").join("README.md")
    readme_file.write("# README")
    was_file_found = gatorgrader_files.check_file_in_directory(
        "README_not_there.md",
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is False
