"""Test cases for the files module"""

from gator import files


def test_create_one_file_path_with_none_middle(tmpdir):
    """Ensure that creating a single file path works correctly"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    created_path = files.create_path(
        tmpdir.basename, file="hello.txt", home=tmpdir.dirname
    )
    assert created_path.name == "hello.txt"
    assert created_path.parent.absolute is not None
    assert created_path.parent.name != "sub"
    assert created_path.parent.name.count("test_") == 1


def test_create_one_file_path_with_one_middle(tmpdir):
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


def test_create_one_file_path_with_two_middle(tmpdir):
    """Ensure that creating a single file path works correctly"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    created_path = files.create_path(
        tmpdir.basename, "subfirst", "subsecond", file="hello.txt", home=tmpdir.dirname
    )
    assert created_path.name == "hello.txt"
    assert created_path.parent.absolute is not None
    assert created_path.parent.name == "subsecond"
    assert created_path.parent.parent.absolute is not None
    assert created_path.parent.parent.name == "subfirst"


def test_one_file_found_in_subdirectory(tmpdir):
    """Ensure that check_file_in_directory can find one file in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True


def test_one_file_found_in_subdirectory_case_sensitivity_ext_csfunction(tmpdir):
    """Ensure that case-sensitive function can find file name in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.case_sensitive_check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # the file should be not found with the uppercase name
    was_file_found = files.case_sensitive_check_file_in_directory(
        tmpdir.basename, "sub", file="hello.TXT", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_one_file_found_in_subdirectory_case_sensitivity_ext(tmpdir):
    """Ensure that check_file_in_directory can find case-sensitive file name in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # the file should be not found with the uppercase name
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.TXT", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_many_files_found_in_subdirectory(tmpdir):
    """Ensure that check_file_in_directory can find many files in a subdirectory"""
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


def test_one_file_found_in_subdirectory_case_sensitivity_csfunction(tmpdir):
    """Ensure that case-sensitive function can find file name in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.case_sensitive_check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # the file should be not found with the uppercase name
    was_file_found = files.case_sensitive_check_file_in_directory(
        tmpdir.basename, "sub", file="HELLO.txt", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_one_file_found_in_subdirectory_case_sensitivity_noncsfunction(tmpdir):
    """Ensure that non-case-sensitive function can find file name in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.case_insensitive_check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # note that checking for the existence of HELLO.txt is an
    # assertion that would not pass across all operating systems


def test_one_file_found_in_subdirectory_case_sensitivity(tmpdir):
    """Ensure that check_file_in_directory can find case-sensitive file name in a subdirectory"""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # the file should be not found with the uppercase name
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="HELLO.txt", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_many_files_found_in_subdirectory(tmpdir):
    """Ensure that check_file_in_directory can find many files in a subdirectory"""
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
