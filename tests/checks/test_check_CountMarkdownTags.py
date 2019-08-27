"""Tests for CountMarkdownTags's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch


from gator import arguments
from gator import checkers
from gator import report
from gator.checks import check_CountMarkdownTags


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_CountMarkdownTags.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 3


@pytest.mark.parametrize(
    "commandline_arguments",
    [
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
    with pytest.raises(SystemExit):
        _ = check_CountMarkdownTags.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 3


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
    with not_raises(SystemExit):
        _ = check_CountMarkdownTags.parse(commandline_arguments)


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
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_CountMarkdownTags.get_parser()
        _ = check_CountMarkdownTags.parse(commandline_arguments, parser)


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
        external_checker_directory = checkers.get_checker_dir(parsed_arguments)
        checker_source = checkers.get_source([external_checker_directory])
        check_name = checkers.get_chosen_check(parsed_arguments)
        check_file = checkers.transform_check(check_name)
        check_exists = checkers.verify_check_existence(check_file, checker_source)
        assert check_exists is True
        check = checker_source.load_plugin(check_file)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is not None
        assert len(check_result) == 1
        # assert check_result[0] is expected_result
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
        external_checker_directory = checkers.get_checker_dir(parsed_arguments)
        checker_source = checkers.get_source([external_checker_directory])
        check_name = checkers.get_chosen_check(parsed_arguments)
        check_file = checkers.transform_check(check_name)
        check_exists = checkers.verify_check_existence(check_file, checker_source)
        assert check_exists is True
        check = checker_source.load_plugin(check_file)
        check_result = check.act(parsed_arguments, remaining_arguments)
        # check the result
        assert check_result is not None
        assert len(check_result) == 1
        # assert check_result[0] is expected_result
        # check the contents of the report
        assert report.get_result() is not None
        assert len(report.get_result()["check"]) > 1
        assert report.get_result()["outcome"] is expected_result
        if expected_result:
            assert report.get_result()["diagnostic"] == ""
        else:
            assert report.get_result()["diagnostic"] != ""
