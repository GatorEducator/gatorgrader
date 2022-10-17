"""Test cases for the orchestrate module."""

import pytest

from gator import orchestrate


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (
            [
                "--description",
                'invalid description with "quotes"',
                "CountCommits",
                "--count",
                "0",
            ]
        ),
        (
            [
                "--checkerdir",
                "/not/a/real/path",
                "CountCommits",
                "--count",
                "0",
            ]
        ),
    ],
)
def test_main_cli_fails_with_incorrect_system_arguments(commandline_arguments, capsys):
    """Ensure that main_cli fails when given an invalid system configuration."""
    with pytest.raises(SystemExit):
        _ = orchestrate.main_cli(commandline_arguments)
    captured = capsys.readouterr()
    print(captured.out)
    counted_newlines = captured.out.count("\n")
    assert captured.err == ""
    assert "Incorrect command-line arguments." in captured.out
    assert counted_newlines == 8


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
    ],
)
def test_main_cli_fails_with_nonexistent_check(commandline_arguments, capsys):
    """Ensure that main_cli fails when given an invalid system configuration."""
    with pytest.raises(SystemExit):
        _ = orchestrate.main_cli(commandline_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert captured.err == ""
    assert "Incorrect command-line arguments." in captured.out
    assert "is not a valid check." in captured.out
    assert counted_newlines == 9


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
    assert counted_newlines == 6
    assert "has exactly" in captured.out or "has at least" in captured.out


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (
            [
                "ListChecks",
                "--listcheckdoesnothave",
                "--fragment",
                "NoFragment",
                "--count",
                "0",
                "--exact",
            ]
        ),
        (
            [
                "CountCommandOutput",
                "--commanddoesnothave",
                'echo "CorrectCommand"',
                "--count",
                "100",
                "--exact",
            ]
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--countdoesnothave",
                "100",
                "--exact",
            ]
        ),
        (
            [
                "CountCommandOutput",
                "--command",
                'echo "CorrectCommand"',
                "--countdoesnothave",
                "100",
                "--exactnotcorrect",
            ]
        ),
    ],
)
def test_check_produces_correct_output_for_incorrect_check_specification(
    capsys, commandline_arguments
):
    """Ensure that using the check produces output."""
    with pytest.raises(SystemExit):
        _ = orchestrate.main_cli(commandline_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert captured.err == ""
    assert "Incorrect check arguments." in captured.out
    assert "usage:" in captured.out
    assert counted_newlines == 11


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
