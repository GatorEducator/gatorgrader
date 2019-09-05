"""Tests for ConfirmFileExists's input and verification of command-line arguments."""

import pytest
import os
import sys

from unittest.mock import patch


from gator import arguments
from gator import report
from gator.checks import check_ConfirmFileExists


def test_no_arguments_incorrect_system_exit(capsys):
    """No command-line arguments causes SystemExit crash of argparse with error output."""
    with pytest.raises(SystemExit):
        _ = check_ConfirmFileExists.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--file"]),
        (["--fileWRONG", "filename"]),
        (["--file", "filename", "--WRONG"]),
        (["--file", "filename", "--directory"]),
        (["--file", "filename", "--directoryWRONG", "directory"]),
    ],
)
def test_required_commandline_arguments_cannot_parse(commandline_arguments, capsys):
    """Check that incorrect optional command-line arguments check correctly."""
    with pytest.raises(SystemExit):
        _ = check_ConfirmFileExists.parse(commandline_arguments)
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 2


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--file", "filename", "--directory", "directoryname"]),
        (["--directory", "directoryname", "--file", "filename"]),
    ],
)
def test_required_commandline_arguments_can_parse(commandline_arguments, not_raises):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        _ = check_ConfirmFileExists.parse(commandline_arguments)


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--file", "filename", "--directory", "directoryname"]),
        (["--directory", "directoryname", "--file", "filename"]),
    ],
)
def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):
    """Check that correct optional command-line arguments check correctly."""
    with not_raises(SystemExit):
        parser = check_ConfirmFileExists.get_parser()
        _ = check_ConfirmFileExists.parse(commandline_arguments, parser)


@pytest.mark.parametrize(
    "commandline_arguments, chosen_file, containing_directory, expected_result",
    [
        (
            [
                "ConfirmFileExists",
                "--file",
                "file_to_find",
                "--directory",
                "containing_directory",
            ],
            "file_to_find",
            "containing_directory",
            True,
        )
    ],
)
def test_act_produces_output(
    commandline_arguments,
    chosen_file,
    containing_directory,
    expected_result,
    tmpdir,
    load_checker,
):
    """Check that using the check produces output."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        new_file = tmpdir.mkdir(containing_directory).join(chosen_file)
        new_file.write("\\begin{document} hello! \\end{document}")
        assert new_file.read() == "\\begin{document} hello! \\end{document}"
        assert len(tmpdir.listdir()) == 1
        overall_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + containing_directory
        )
        commandline_arguments = [
            "ConfirmFileExists",
            "--file",
            "file_to_find",
            "--directory",
            overall_directory,
        ]
        parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check_exists, checker_source, check_file = load_checker(parsed_arguments)
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
