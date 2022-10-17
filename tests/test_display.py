"""Tests for the display module.."""

from gator import display
from gator.exceptions import InvalidCheckArgumentsError, InvalidCheckError


def test_display_welcome_produce_output_line_count(capsys):
    """Check that the display welcome function produces output lines."""
    display.welcome_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "github.com" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


def test_display_invalid_system_arguments(capsys):
    """Check that the invalid system arguments function produces output lines."""
    display.incorrect_system_arguments_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


def test_display_invalid_system_arguments_with_error(capsys):
    """Check that the invalid system arguments function produces output lines."""
    display.incorrect_system_arguments_message(InvalidCheckError([], "TestCheck"))
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect command-line" in captured.out
    assert "TestCheck" in captured.out
    assert counted_newlines == 3
    assert captured.err == ""


def test_display_invalid_check_arguments(capsys):
    """Check that the invalid check arguments function produces output lines."""
    display.incorrect_check_arguments_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect check" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


def test_display_invalid_check_arguments_with_error(capsys):
    """Check that the invalid check arguments function produces output lines."""
    display.incorrect_check_arguments_message(
        InvalidCheckArgumentsError(
            [], "usage: TestCheck", "TestCheck: some error happened"
        )
    )
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect check" in captured.out
    assert "usage:" in captured.out
    assert captured.out.count("TestCheck") == 2
    assert "some error" in captured.out
    assert counted_newlines == 5
    assert captured.err == ""


def test_reminder_produce_output_line_count(capsys):
    """Check that the help reminder function produces output lines."""
    display.help_reminder()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "--help" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


def test_display_message_with_newline(capsys):
    """Check that the message function produces output lines."""
    display.message("Example message")
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Example message" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


def test_display_message_with_additional_newline(capsys):
    """Check that the message function produces output lines."""
    display.message("Example message\n")
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Example message" in captured.out
    assert counted_newlines == 3
    assert captured.err == ""
