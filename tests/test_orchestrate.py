"""Test cases for the orchestrate module."""

import pytest
import os
import sys

from unittest.mock import patch

from gator import constants
from gator import orchestrate
from gator import report


def test_perform_actions_no_parameters_welcome(capsys):
    """Check to see if perform can invoke welcome action with no parameters."""
    actions = []
    actions.append([orchestrate.DISPLAY, "welcome_message", []])
    orchestrate.perform_actions(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


def test_perform_actions_no_parameters_incorrect(capsys):
    """Check to see if perform can invoke incorrect action with no parameters."""
    actions = []
    actions.append([orchestrate.DISPLAY, "incorrect_message", []])
    orchestrate.perform_actions(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


def test_perform_actions_single_parameter_exit():
    """Check to see if perform can invoke exit actions with a parameter."""
    actions = []
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        actions.append([orchestrate.RUN, "run_exit", [constants.arguments.Incorrect]])
        orchestrate.perform_actions(actions)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@pytest.mark.parametrize(
    "commandline_arguments, expected_result",
    [
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
            ],
            0,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
                "--exact",
            ],
            0,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "1000",
            ],
            1,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "1000",
                "--exact",
            ],
            1,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "1",
            ],
            0,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "2",
                "--exact",
            ],
            1,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "100",
            ],
            1,
        ),
        (
            [
                "MatchCommandFragment",
                "--command",
                'echo "CorrectCommand"',
                "--fragment",
                "Corr",
                "--count",
                "100",
                "--exact",
            ],
            1,
        ),
    ],
)
def test_check_produces_correct_output(commandline_arguments, expected_result, capsys):
    """Ensure that using the check produces output."""
    check_exit_code = orchestrate.main_cli(commandline_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert check_exit_code == expected_result
    assert captured.err == ""
    assert captured.out != ""
    assert counted_newlines > 5
    assert "has exactly" in captured.out or "has at least" in captured.out


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (
            [
                "CheckDoesNotExist",
                "--command",
                "WrongCommand",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
            ],
        ),
        (
            [
                "ListCheck",
                "--listcheckdoesnothave",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
                "--exact",
            ],
        ),
        (
            [
                "CountCommandOutput",
                "--commanddoesnothave",
                'echo "CorrectCommand"',
                "--count",
                "100",
                "--exact",
            ],
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--countdoesnothave",
                "100",
                "--exact",
            ],
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--countdoesnothave",
                "100",
                "--exactnotcorrect",
            ],
        ),
    ],
)
def test_check_produces_correct_output_for_incorrect_check_specification(
    commandline_arguments, capsys
):
    """Ensure that using the check produces output."""
    with pytest.raises(SystemExit):
        _ = orchestrate.main_cli(commandline_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert captured.err == ""
    assert "Incorrect command-line arguments." in captured.out
    assert counted_newlines > 5


def test_main_cli_produces_welcome_message(capsys):
    """Ensure that a regular check produces a welcome message."""
    exit_code = orchestrate.main_cli(
        [
            "CountCommits",
            "--count",
            "0",
        ],
    )
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert exit_code == 0
    assert counted_newlines == 6
    assert "GatorGrader" in captured.out
    assert captured.err == ""


def test_main_cli_produces_no_welcome_message(capsys):
    """Ensure that a regular check produces a no welcome message when requested."""
    exit_code = orchestrate.main_cli(
        [
            "--nowelcome",
            "CountCommits",
            "--count",
            "0",
        ],
    )
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert exit_code == 0
    assert counted_newlines == 2
    assert "GatorGrader" not in captured.out
    assert captured.err == ""


def test_main_cli_fails_with_incorrect_system_arguments(capsys):
    """Ensure that main_cli fails when given an invalid system configuration."""
    with pytest.raises(SystemExit):
        _ = orchestrate.main_cli(
            [
                "--description",
                'invalid description with "quotes"',
                "CountCommits",
                "--count",
                "0",
            ],
        )
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert captured.err == ""
    assert "Incorrect command-line arguments." in captured.out
    assert counted_newlines > 5
