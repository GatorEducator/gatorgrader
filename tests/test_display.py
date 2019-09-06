"""Tests for the display module.."""

from gator import display


def test_display_welcome_produce_output_line_count(capsys):
    """Check that the display welcome function produces output lines."""
    display.welcome_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "github.com" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


def test_display_checking_produce_output_line_count(capsys):
    """Check that the display checking function produces output lines."""
    display.checking_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Valid" in captured.out
    assert counted_newlines == 3
    assert captured.err == ""


def test_dislay_invalid_produce_output_line_count(capsys):
    """Check that the invalid arguments function produces output lines."""
    display.incorrect_message()
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
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
