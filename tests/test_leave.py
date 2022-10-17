"""Test cases for the leave module.."""

from gator import leave


def test_failing_exit():
    """Check that code is failing."""
    failing_code = leave.get_code(False)
    assert failing_code == 1


def test_passing_exit():
    """Check that code is passing."""
    passing_code = leave.get_code(True)
    assert passing_code == 0
