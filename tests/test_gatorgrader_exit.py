""" test cases for the gatorgrader_exit module """

import pytest

import gatorgrader_exit


def test_failing_exit():
    """Checks that code fails"""
    failing_exit = [True, True, False]
    failing_code = gatorgrader_exit.get_code(failing_exit)
    assert failing_code == 1

def test_failing_exit_different():
    """that true input returns yes"""
    failing_exit = [True, True, False]
    failing_code = gatorgrader_exit.get_code(failing_exit)
    assert failing_code == 1

@pytest.mark.parametrize("return_values,expected_codes", [
    ([True], 0),
    ([False], 1),
    ([True, True], 0),
])
def test_exit_codes_parameterized(return_values, expected_codes):
    assert gatorgrader_exit.get_code(return_values) == expected_codes
