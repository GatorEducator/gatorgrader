"""Test cases for the files module."""

import platform

from gator import files

# define the operating systems on which to run processes
LINUX = "Linux"
MAC = "Darwin"
WINDOWS = "Windows"


# Region: Glob Tests for create_paths {{{


def test_create_one_glob_path_with_none_middle(tmpdir):
    """Ensure that creating a globbed path works correctly."""
    hello_file_one = tmpdir.join("hello1.txt")
    hello_file_one.write("content")
    hello_file_two = tmpdir.join("hello2.txt")
    hello_file_two.write("content")
    assert len(tmpdir.listdir()) == 2
    created_paths = list(
        files.create_paths(tmpdir.basename, file="*.txt", home=tmpdir.dirname)
    )
    assert len(created_paths) == 2
    for created_path in files.create_paths(
        tmpdir.basename, file="*.txt", home=tmpdir.dirname
    ):
        assert ".txt" in str(created_path)
    created_paths = list(
        files.create_paths(tmpdir.basename, file="hello*", home=tmpdir.dirname)
    )
    assert len(created_paths) == 2
    for created_path in files.create_paths(
        tmpdir.basename, file="hello*", home=tmpdir.dirname
    ):
        assert ".txt" in str(created_path)


def test_create_non_glob_path_with_none_middle(tmpdir):
    """Ensure that creating a non-globbed path with get_paths works correctly."""
    hello_file_one = tmpdir.join("hello1.txt")
    hello_file_one.write("content")
    hello_file_two = tmpdir.join("hello2.txt")
    hello_file_two.write("content")
    assert len(tmpdir.listdir()) == 2
    created_paths = list(
        files.create_paths(tmpdir.basename, file="hello1.txt", home=tmpdir.dirname)
    )
    assert len(created_paths) == 1
    created_paths = list(
        files.create_paths(tmpdir.basename, file="hello2.txt", home=tmpdir.dirname)
    )
    assert len(created_paths) == 1


def test_one_glob_case_sensitive_handling(tmpdir):
    """Ensure that creating a non-matching globbed path does not return paths."""
    hello_file_one = tmpdir.join("hello1.txt")
    hello_file_one.write("content")
    hello_file_two = tmpdir.join("hello2.txt")
    hello_file_two.write("content")
    system_name = platform.system()
    if system_name is LINUX or MAC:
        assert len(tmpdir.listdir()) == 2
        created_paths = list(
            files.create_paths(tmpdir.basename, file="*.TXT", home=tmpdir.dirname)
        )
        assert len(created_paths) == 0
    elif system_name is WINDOWS:
        assert len(tmpdir.listdir()) == 2
        created_paths = list(
            files.create_paths(tmpdir.basename, file="*.TXT", home=tmpdir.dirname)
        )
        assert len(created_paths) == 0
    if system_name is LINUX or MAC:
        for created_path in files.create_paths(
            tmpdir.basename, file="HELLO*", home=tmpdir.dirname
        ):
            assert ".txt" in str(created_path)
        assert len(created_paths) == 0
    elif system_name is WINDOWS:
        for created_path in files.create_paths(
            tmpdir.basename, file="HELLO*", home=tmpdir.dirname
        ):
            assert ".txt" in str(created_path)
        assert len(created_paths) == 2


def test_garbage_glob_returns_no_matching_paths(tmpdir):
    """Ensure that creating a garbage globbed path returns no matches."""
    hello_file_one = tmpdir.join("hello1.txt")
    hello_file_one.write("content")
    hello_file_two = tmpdir.join("hello2.txt")
    hello_file_two.write("content")
    assert len(tmpdir.listdir()) == 2
    created_paths = list(
        files.create_paths(tmpdir.basename, file="FAKE&&&FDF$$#**", home=tmpdir.dirname)
    )
    assert len(created_paths) == 0
    for created_path in files.create_paths(
        tmpdir.basename, file="FAKE&&&FDF$$#**", home=tmpdir.dirname
    ):
        assert ".txt" in str(created_path)
    assert len(created_paths) == 0


# }}}


# Region: Non-Glob Tests for create_path {{{


def test_create_one_file_path_with_none_middle(tmpdir):
    """Ensure that creating a single file path works correctly."""
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
    """Ensure that creating a single file path works correctly."""
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
    """Ensure that creating a single file path works correctly."""
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
    """Ensure that check_file_in_directory can find one file in a subdirectory."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True


def test_one_file_found_in_subdirectory_case_sensitivity_ext_csfunction(tmpdir):
    """Ensure that case-sensitive function can find file name in a subdirectory."""
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
    """Ensure that check_file_in_directory can find case-sensitive file name in a subdirectory."""
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


def test_one_file_found_in_subdirectory_case_sensitivity_csfunction(tmpdir):
    """Ensure that case-sensitive function can find file name in a subdirectory."""
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
    """Ensure that non-case-sensitive function can find file name in a subdirectory."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # the file should be found with the lowercase name
    was_file_found = files.case_native_check_file_in_directory(
        tmpdir.basename, "sub", file="hello.txt", home=tmpdir.dirname
    )
    assert was_file_found is True
    # note that checking for the existence of HELLO.txt is an
    # assertion that would not pass across all operating systems


def test_one_file_found_in_subdirectory_case_sensitivity(tmpdir):
    """Ensure that check_file_in_directory can find case-sensitive file name in a subdirectory."""
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
    """Ensure that check_file_in_directory can find many files in a subdirectory."""
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


def test_many_files_in_subdirectory_casesensitive(tmpdir):
    """Ensure that check_file_in_directory can find many files in a subdirectory."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # case sensitive found
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
    # case sensitive not found
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="HELLO.TXT", home=tmpdir.dirname
    )
    assert was_file_found is False
    readme_file = tmpdir.join("sub").join("README.md")
    readme_file.write("# README")
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="README.MD", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_one_file_not_found_in_subdirectory(tmpdir):
    """Ensure check_file_in_directory cannot find one file in a subdirectory."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="hello_not_there.txt", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_one_file_not_found_in_subdirectory_casesensitive(tmpdir):
    """Ensure check_file_in_directory cannot find one file in a subdirectory."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="HELLO_NOT_THERE.TXT", home=tmpdir.dirname
    )
    assert was_file_found is False
    was_file_found = files.check_file_in_directory(
        tmpdir.basename, "sub", file="HELLO.TXT", home=tmpdir.dirname
    )
    assert was_file_found is False


def test_many_files_not_found_in_subdirectory(tmpdir):
    """Ensure check_file_in_directory cannot find many files in a subdirectory."""
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


# }}}
