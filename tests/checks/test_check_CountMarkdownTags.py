"""Tests for CountMarkdownTags's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch


from gator import arguments
from gator import report
from gator.exceptions import InvalidCheckArgumentsError
from gator.checks import check_CountMarkdownTags


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        ([]),
        (["--file"]),
        (["--fileWRONG", "filename"]),
        (["--file", "filename", "--WRONG"]),
        (["--file", "filename", "--directory"]),
        (["--file", "filename", "--directoryWRONG", "directory"]),
        (["--file", "filename", "--directory", "directory", "--count"]),
        (["--file", "filename", "--directory", "directory", "--countWRONG", "5"]),
        (["--file", "filename", "--directory", "directory", "--count", "--tag"]),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--tagWRONG",
                "code",
            ]
        ),
    ],
)
def test_required_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(InvalidCheckArgumentsError) as excinfo:
        _ = check_CountMarkdownTags.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output or error
    assert captured.err == ""
    assert captured.out == ""
    assert excinfo.value.check_name == "CountMarkdownTags"
    assert excinfo.value.usage
    assert excinfo.value.error


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (
            [
                "--file",
                "filename",
                "--directory",
                "directoryname",
                "--count",
                "5",
                "--tag",
                "code",
            ]
        ),
        (
            [
                "--directory",
                "directoryname",
                "--file",
                "filename",
                "--count",
                "5",
                "--tag",
                "code",
            ]
        ),
        (
            [
                "--tag",
                "code",
                "--count",
                "5",
                "--directory",
                "directoryname",
                "--file",
                "filename",
            ]
        ),
        (
            [
                "--directory",
                "directoryname",
                "--tag",
                "code",
                "--count",
                "5",
                "--file",
                "filename",
            ]
        ),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(InvalidCheckArgumentsError):
        _ = check_CountMarkdownTags.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments, chosen_file, containing_directory, provided_count, expected_result",
    [
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "5",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "5",
            True,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "100",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "5",
                "--exact",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "5",
            True,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "100",
                "--exact",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
    ],
)
def test_act_produces_output(
    commandline_arguments,
    chosen_file,
    containing_directory,
    provided_count,
    expected_result,
    tmpdir,
    load_check,
):
    """Check that using the check produces output."""
    test_contents = """
## What Do People Think about GatorGrader?

GatorGrader addresses many of the challenges that an instructor faces when
designing automated checks for the source code or technical writing that a

## Installing GatorGrader

Installing GatorGrader is not necessary if you intend to use it through its
[Gradle plugin](https://github.com/GatorEducator/gatorgradle). If you want to

## Running GatorGrader

Students and instructors normally use GatorGrader through its [Gradle
plugin](https://github.com/GatorEducator/gatorgradle), specifying the requested

## Testing GatorGrader

### Automated Testing

The developers use [Pytest](https://docs.pytest.org/en/latest/) for the testing
of GatorGrader. Depending on your goals, there are several different..."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        new_file = tmpdir.mkdir(containing_directory).join(chosen_file)
        new_file.write(test_contents)
        assert new_file.read() == test_contents
        assert len(tmpdir.listdir()) == 1
        overall_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + containing_directory
        )
        commandline_arguments = [
            "CountMarkdownTags",
            "--file",
            "file_to_find",
            "--directory",
            overall_directory,
            "--count",
            provided_count,
            "--tag",
            "heading",
        ]
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is expected_result
        # check the contents of the report
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is expected_result
        if expected_result:
            assert report.get_result()["diagnostic"] == ""
        else:
            assert report.get_result()["diagnostic"] != ""


@pytest.mark.parametrize(
    "commandline_arguments, chosen_file, containing_directory, provided_count, expected_result",
    [
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "5",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "5",
            True,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "100",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "5",
                "--exact",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "5",
            True,
        ),
        (
            [
                "CountMarkdownTags",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--count",
                "100",
                "--exact",
                "--tag",
                "heading",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
    ],
)
def test_act_produces_output_with_exact(
    commandline_arguments,
    chosen_file,
    containing_directory,
    provided_count,
    expected_result,
    tmpdir,
    load_check,
):
    """Check that using the check produces output."""
    test_contents = """
## What Do People Think about GatorGrader?

GatorGrader addresses many of the challenges that an instructor faces when
designing automated checks for the source code or technical writing that a

## Installing GatorGrader

Installing GatorGrader is not necessary if you intend to use it through its
[Gradle plugin](https://github.com/GatorEducator/gatorgradle). If you want to

## Running GatorGrader

Students and instructors normally use GatorGrader through its [Gradle
plugin](https://github.com/GatorEducator/gatorgradle), specifying the requested

## Testing GatorGrader

### Automated Testing

The developers use [Pytest](https://docs.pytest.org/en/latest/) for the testing
of GatorGrader. Depending on your goals, there are several different..."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        new_file = tmpdir.mkdir(containing_directory).join(chosen_file)
        new_file.write(test_contents)
        assert new_file.read() == test_contents
        assert len(tmpdir.listdir()) == 1
        overall_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + containing_directory
        )
        commandline_arguments = [
            "CountMarkdownTags",
            "--file",
            "file_to_find",
            "--directory",
            overall_directory,
            "--count",
            provided_count,
            "--tag",
            "heading",
            "--exact",
        ]
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is expected_result
        # check the contents of the report
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is expected_result
        if expected_result:
            assert report.get_result()["diagnostic"] == ""
        else:
            assert report.get_result()["diagnostic"] != ""
