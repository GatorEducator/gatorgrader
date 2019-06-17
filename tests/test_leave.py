"""Test cases for the leave module.."""

import pytest

from gator import leave


def test_failing_exit():
    """Check that code fails."""
    failing_exit = [True, True, False]
    failing_code = leave.get_code(failing_exit)
    assert failing_code == 1


def test_failing_exit_different():
    """Check that true input returns yes."""
    failing_exit = [True, True, False]
    failing_code = leave.get_code(failing_exit)
    assert failing_code == 1


@pytest.mark.parametrize(
    "return_values,expected_codes",
    [
        ([], 0),
        ([True], 0),
        ([False], 1),
        ([True, True], 0),
        ([True, False], 1),
        ([True, False, True], 1),
        ([False, False, False], 1),
        ([True, True, True], 0),
    ],
)
def test_exit_codes_parameterized(return_values, expected_codes):
    """Check that multiple outputs lead to correct exit codes."""
    assert leave.get_code(return_values) == expected_codes
