""" test cases for the gatorgrader_exit module """

import pytest

import gatorgrader_exit


def test_failing_exit():
    """Checks that code fails"""
    failing_exit = [True, True, False]
    failing_code = gatorgrader_exit.get_code(failing_exit)
    assert failing_code == 1


def test_failing_exit_different():
    """Check that true input returns yes"""
    failing_exit = [True, True, False]
    failing_code = gatorgrader_exit.get_code(failing_exit)
    assert failing_code == 1


@pytest.mark.parametrize("return_values,expected_codes", [
    ([], 0),
    ([True], 0),
    ([False], 1),
    ([True, True], 0),
    ([True, False], 1),
    ([True, False, True], 1),
    ([False, False, False], 1),
    ([True, True, True], 0),
])
def test_exit_codes_parameterized(return_values, expected_codes):
    """Check that multiple outputs lead to correct exit codes"""
    assert gatorgrader_exit.get_code(return_values) == expected_codes
