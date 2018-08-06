"""Tests for the display functions"""

import pytest

from gator import display


def test_display_welcome_produce_output_line_count(capsys):
    """Check that the display welcome function produces output lines"""
    display.welcome_message()
    captured = capsys.readouterr()
    assert "github.com" in captured.out
    assert captured.err == ""
