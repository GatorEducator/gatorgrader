"""Tests for CountSingleLineComments's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch


from gator import arguments
from gator import report
from gator.exceptions import InvalidCheckArgumentsError
from gator.checks import check_CountSingleLineComments


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
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--language",
            ]
        ),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--language",
                "PythonNotLanguage",
            ]
        ),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--language",
                "JavaNotLanguage",
            ]
        ),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--languageWRONG",
                "Java",
            ]
        ),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directory",
                "--count",
                "5",
                "--languageWRONG",
                "Python",
            ]
        ),
    ],
)
def test_required_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(InvalidCheckArgumentsError) as excinfo:
        _ = check_CountSingleLineComments.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output or error
    assert captured.err == ""
    assert captured.out == ""
    assert excinfo.value.check_name == "CountSingleLineComments"
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
                "--language",
                "Python",
            ]
        ),
        (
            [
                "--file",
                "filename",
                "--directory",
                "directoryname",
                "--count",
                "5",
                "--language",
                "Java",
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
                "--language",
                "Python",
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
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--count",
                "5",
                "--directory",
                "directoryname",
                "--file",
                "filename",
                "--language",
                "Python",
            ]
        ),
        (
            [
                "--directory",
                "directoryname",
                "--count",
                "5",
                "--file",
                "filename",
                "--language",
                "Java",
            ]
        ),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(InvalidCheckArgumentsError):
        _ = check_CountSingleLineComments.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments, chosen_file, containing_directory, provided_count, expected_result",
    [
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Python",
                "--count",
                "1",
            ],
            "file_to_find",
            "containing_directory",
            "1",
            True,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Python",
                "--count",
                "100",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Python",
                "--count",
                "1",
                "--exact",
            ],
            "file_to_find",
            "containing_directory",
            "1",
            True,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Python",
                "--count",
                "100",
                "--exact",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
    ],
)
def test_act_produces_output_python(
    commandline_arguments,
    chosen_file,
    containing_directory,
    provided_count,
    expected_result,
    tmpdir,
    load_check,
):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        new_file = tmpdir.mkdir(containing_directory).join(chosen_file)
        new_file.write("# this is a nice Python comment")
        assert new_file.read() == "# this is a nice Python comment"
        assert len(tmpdir.listdir()) == 1
        overall_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + containing_directory
        )
        commandline_arguments = [
            "CountSingleLineComments",
            "--file",
            "file_to_find",
            "--directory",
            overall_directory,
            "--count",
            provided_count,
            "--language",
            "Python",
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
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Java",
                "--count",
                "1",
            ],
            "file_to_find",
            "containing_directory",
            "1",
            True,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Java",
                "--count",
                "100",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Java",
                "--count",
                "1",
                "--exact",
            ],
            "file_to_find",
            "containing_directory",
            "1",
            True,
        ),
        (
            [
                "CountSingleLineComments",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
                "--language",
                "Java",
                "--count",
                "100",
                "--exact",
            ],
            "file_to_find",
            "containing_directory",
            "100",
            False,
        ),
    ],
)
def test_act_produces_output_java(
    commandline_arguments,
    chosen_file,
    containing_directory,
    provided_count,
    expected_result,
    tmpdir,
    load_check,
):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        new_file = tmpdir.mkdir(containing_directory).join(chosen_file)
        new_file.write("// this is a nice Java comment")
        assert new_file.read() == "// this is a nice Java comment"
        assert len(tmpdir.listdir()) == 1
        overall_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + containing_directory
        )
        commandline_arguments = [
            "CountSingleLineComments",
            "--file",
            "file_to_find",
            "--directory",
            overall_directory,
            "--count",
            provided_count,
            "--language",
            "Java",
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
