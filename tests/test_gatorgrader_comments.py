""" test cases for the gatorgrader_utils module """

import pytest

import gatorgrader_comments


@pytest.mark.parametrize("code_string,expected_count", [
    ('//// hello world', 1),
])
def test_exit_codes_parameterized(code_string, expected_count):
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count
