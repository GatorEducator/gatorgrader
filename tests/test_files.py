"""Test cases for the files module"""

from gator import files


def test_create_one_file_path(tmpdir):
    """Ensure that creating a single file path works correctly"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    created_path = files.create_path(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert created_path.name == "hello.txt"
    assert created_path.parent.absolute is not None
    assert created_path.parent.name == "sub"


def test_one_file_found_in_subdirectory(tmpdir):
    """Ensure that check_file_in_directory can find one file file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True


def test_many_files_found_in_subdirectory(tmpdir):
    """Ensure that check_file_in_directory can find many files file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    readme_file = tmpdir.join("sub").join("README.md")
    readme_file.write("# README")
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="README.md", home=tmpdir.dirname
    )
    assert was_file_found is True


def test_one_file_not_found_in_subdirectory(tmpdir):
    """Ensure check_file_in_directory cannot find one file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello_not_there.txt", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_many_files_not_found_in_subdirectory(tmpdir):
    """Ensure check_file_in_directory cannot find many files in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello_not_there.txt", home=tmpdir.dirname
    )
    assert was_file_found is False
    readme_file = tmpdir.join("sub").join("README.md")
    readme_file.write("# README")
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="README_not_there.md", home=tmpdir.dirname
    )
    assert was_file_found is False
