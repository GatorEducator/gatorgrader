"""Test cases for the invoke module.."""

import os
import pytest
import sys

from unittest.mock import patch

from gator import constants
from gator import fragments
from gator import invoke
from gator import report


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary."""
    report.reset()


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_commit_checks(reset_results_dictionary):
    """Check that invocation of commit check works correctly."""
    invoke.invoke_commits_check(".", sys.maxsize)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_commit_checks_exact(reset_results_dictionary):
    """Check that invocation of commit check exacted works correctly."""
    invoke.invoke_commits_check(".", sys.maxsize, True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check(reset_results_dictionary, tmpdir):
    """Check that invocation of file existence check works correctly."""
    hello_file = tmpdir.mkdir("sub").join("hello.txt")
    hello_file.write("content")
    assert hello_file.read() == "content"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    hello_file = "hello.txt"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    # file is found in the specified directory
    assert details is not None
    assert details[constants.results.Outcome] is True
    assert "exists in" in details[constants.results.Description]
    assert details[constants.results.Diagnostic] == ""


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_test_file(reset_results_dictionary):
    """Check that invocation of file existence check works correctly."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        directory = "tests"
        test_file = "test_invoke.py"
        invoke.invoke_file_in_directory_check(test_file, directory)
        details = report.get_result()
        # file is found in the specified directory
        assert details is not None
        assert details[constants.results.Outcome] is True
        assert "exists in" in details[constants.results.Description]
        assert details[constants.results.Diagnostic] == ""


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_paragraphs(reset_results_dictionary, tmpdir):
    """Check that the checking of paragraphs works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write("hello world 44\n\nhi\n\nff!$@name\n\n^^44")
    assert reflection_file.read() == "hello world 44\n\nhi\n\nff!$@name\n\n^^44"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_paragraph_checks(reflection_file, directory, 4)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_paragraph_checks(reflection_file, directory, 200)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_file_exists_in_directory_check_paragraphs_exact(
    reset_results_dictionary, tmpdir
):
    """Check that the checking of paragraphs works for exact correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write("hello world 44\n\nhi\n\nff!$@name\n\n^^44")
    assert reflection_file.read() == "hello world 44\n\nhi\n\nff!$@name\n\n^^44"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_paragraph_checks(reflection_file, directory, 4, True)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_paragraph_checks(reflection_file, directory, 200, True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_words(reset_results_dictionary, tmpdir):
    """Check that the checking of words works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        4,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        200,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_words_no_matching_file(
    reset_results_dictionary, tmpdir
):
    """Check that the checking of words works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflectionWRONG.md"
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        4,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        200,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_words_exact(reset_results_dictionary, tmpdir):
    """Check that the checking of words works exact correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        4,
        fragments.count_minimum_words,
        constants.words.Minimum,
        True,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        200,
        fragments.count_minimum_words,
        constants.words.Minimum,
        True,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_total_words(reset_results_dictionary, tmpdir):
    """Check that the checking of total words works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        12,
        fragments.count_total_words,
        constants.words.Total,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        100,
        fragments.count_total_words,
        constants.words.Total,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_total_words_file_not_exists(
    reset_results_dictionary, tmpdir
):
    """Check that the checking of total words works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflectionWRONG.md"
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        12,
        fragments.count_total_words,
        constants.words.Total,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        100,
        fragments.count_total_words,
        constants.words.Total,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_total_words_exact(
    reset_results_dictionary, tmpdir
):
    """Check that the checking of total words works exactly correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    # invoke.invoke_all_total_word_count_checks(
    # reflection_file, directory, 12, exact=True
    # )
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        12,
        fragments.count_total_words,
        constants.words.Total,
        exact=True,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    # invoke.invoke_all_total_word_count_checks(
    # reflection_file, directory, 100, exact=True
    # )
    invoke.invoke_all_total_word_count_checks(
        reflection_file,
        directory,
        100,
        fragments.count_total_words,
        constants.words.Total,
        exact=True,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_words_wildcards(
    reset_results_dictionary, tmpdir
):
    """Check that the checking of words works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "*.md"
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        4,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_minimum_word_count_checks(
        reflection_file,
        directory,
        200,
        fragments.count_minimum_words,
        constants.words.Minimum,
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_fragments(reset_results_dictionary, tmpdir):
    """Check that the checking of fragments in a file works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_fragment_checks("hello", 1, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_fragment_checks("@name", 1, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_fragment_checks("again", 2, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_fragment_checks("planet", 2, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_fragments_exact(
    reset_results_dictionary, tmpdir
):
    """Check that the exact checking of fragments in a file works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_fragment_checks("hello", 1, reflection_file, directory, "", True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_regex_exact(reset_results_dictionary, tmpdir):
    """Check that the exact checking of fragments in a file works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_regex_checks(
        r"fine(.*?)nice\sagain", 1, reflection_file, directory, "", True
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_content_string_check_fragments(reset_results_dictionary):
    """Check that the checking of words works correctly."""
    value = "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    invoke.invoke_all_fragment_checks("hello", 1, contents=value)
    invoke.invoke_all_fragment_checks("@name", 1, contents=value)
    invoke.invoke_all_fragment_checks("@name", 2, contents=value)
    invoke.invoke_all_fragment_checks("planet", 2, contents=value)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_content_string_check_fragments_exact(reset_results_dictionary):
    """Check that the checking of exact fragments works correctly."""
    value = "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    invoke.invoke_all_fragment_checks("hello", 1, contents=value, exact=True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_content_string_check_regex_exact(reset_results_dictionary):
    """Check that the checking of exact regex works correctly."""
    value = "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    invoke.invoke_all_regex_checks("hello", 1, contents=value, exact=True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_lines(reset_results_dictionary, tmpdir):
    """Check that the checking of lines in a file works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_count_checks(1, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_count_checks(100, reflection_file, directory, "")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_file_exists_in_directory_check_lines_exact(reset_results_dictionary, tmpdir):
    """Check that the checking of lines in a file works correctly."""
    reflection_file = tmpdir.mkdir("sub").join("reflection.md")
    reflection_file.write(
        "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert (
        reflection_file.read()
        == "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub"
    reflection_file = "reflection.md"
    invoke.invoke_all_count_checks(1, reflection_file, directory, "", True)
    invoke.invoke_all_count_checks(100, reflection_file, directory, "", True)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_content_string_check_fragments_with_threshold(reset_results_dictionary):
    """Check that the checking of words works correctly."""
    value = "hello world 44 fine\n\nhi there nice again\n\nff! Is now $@name again\n\n"
    invoke.invoke_all_count_checks(1, contents=value)
    invoke.invoke_all_count_checks(2, contents=value)
    invoke.invoke_all_count_checks(7, contents=value)
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_single_java(reset_results_dictionary, tmpdir):
    """Check to that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("//// hello world")
    assert hello_file.read() == "//// hello world"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(hello_file, directory, 1, "single-line", "Java")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_single_java_exact(reset_results_dictionary, tmpdir):
    """Check to that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("//// hello world")
    assert hello_file.read() == "//// hello world"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(
        hello_file, directory, 1, "single-line", "Java", True
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_single_python(reset_results_dictionary, tmpdir):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    hello_file.write("# hello world")
    assert hello_file.read() == "# hello world"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.py"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(hello_file, directory, 1, "single-line", "Python")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_multiple_java(reset_results_dictionary, tmpdir):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(hello_file, directory, 1, "multiple-line", "Java")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_multiple_java_invalid_check(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    # this check cannot pass because of the fact that it asks
    # for "standard-line" comments, which are not supported by this function
    invoke.invoke_all_comment_checks(hello_file, directory, 1, "standard-line", "Java")
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_comment_counts_check_multiple_java_not_enough(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(
        hello_file, directory, 100, "multiple-line", "Java"
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_comment_counts_check_multiple_python(reset_results_dictionary, tmpdir):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    hello_file.write('""" hello world """')
    assert hello_file.read() == '""" hello world """'
    assert len(tmpdir.listdir()) == 1
    # directory = tmpdir.dirname + '"""' + tmpdir.basename + '"""' + "subdirectory"
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.py"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(
        hello_file, directory, 1, "multiple-line", "Python"
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_comment_counts_check_multiple_python_not_enough(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of comment counting check works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    hello_file.write('""" hello world """')
    assert hello_file.read() == '""" hello world """'
    assert len(tmpdir.listdir()) == 1
    # directory = tmpdir.dirname + '"""' + tmpdir.basename + '"""' + "subdirectory"
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.py"
    invoke.invoke_file_in_directory_check(hello_file, directory)
    details = report.get_result()
    assert details is not None
    report.reset()
    invoke.invoke_all_comment_checks(
        hello_file, directory, 100, "multiple-line", "Python"
    )
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_grab_output_as_string(reset_results_dictionary, tmpdir):
    """Check that invocation of command produces correct captured output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    met_or_exceeded_count = invoke.invoke_all_command_fragment_checks(
        "ls " + directory, "Hello1", 1
    )
    assert met_or_exceeded_count is True
    details = report.get_result()
    assert details is not None
    report.reset()
    met_or_exceeded_count = invoke.invoke_all_command_fragment_checks(
        "ls " + directory, "HelloNotThere", 1
    )
    assert met_or_exceeded_count is False
    met_or_exceeded_count = invoke.invoke_all_command_fragment_checks(
        "ls " + directory, "HelloNotThere", 0
    )
    assert met_or_exceeded_count is True


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_grab_output_as_string_count_lines(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of command produces correct captured output for line count."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    met_or_exceeded_count = invoke.invoke_all_command_count_checks("ls " + directory, 1)
    assert met_or_exceeded_count is True
    met_or_exceeded_count = invoke.invoke_all_command_count_checks("ls " + directory, 4)
    assert met_or_exceeded_count is False
    details = report.get_result()
    assert details is not None


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_grab_output_as_string_count_lines_exact(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of command produces correct captured output for exact line count."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    met_or_exceeded_count = invoke.invoke_all_command_count_checks(
        "ls " + directory, 3, True
    )
    assert met_or_exceeded_count is True
    met_or_exceeded_count = invoke.invoke_all_command_count_checks(
        "ls " + directory, 4, True
    )
    assert met_or_exceeded_count is False
    details = report.get_result()
    assert details is not None


def test_command_executes_checks_does_not_execute_correctly():
    """Check to see if a command does not run correctly and gets a zero return value."""
    # note that a zero-code means that the command did not work
    # this is the opposite of what is used for processes
    # but, all other GatorGrader checks return 0 on failure and 1 on success
    status_code = invoke.invoke_all_command_executes_checks("willnotwork")
    assert status_code is False


def test_command_executes_checks_does_execute_correctly():
    """Check to see if a command does run correctly and gets a non-zero return value."""
    # note that a zero-code means that the command did not work
    # this is the opposite of what is used for processes
    # but, all other GatorGrader checks return 0 on failure and 1 on success
    status_code = invoke.invoke_all_command_executes_checks("true")
    assert status_code is True


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_does_execute_correctly_would_make_output(
    reset_results_dictionary, tmpdir
):
    """Check that invocation of command runs when it makes output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    executed_yes = invoke.invoke_all_command_executes_checks("ls " + directory)
    assert executed_yes is True
