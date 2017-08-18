""" test cases for the gatorgrader_utils module """

import pytest

import gatorgrader_comments


@pytest.mark.parametrize("code_string,expected_count", [
    ('//// hello world', 1),
    ('//// hello // world', 1),
    ('//// hello //// world', 1),
    ('// hello world', 1),
    ('// hello world && --', 1),
    ('// hello world  __ --', 1),
    (r'System.out.println("Hello, World!\n"); // prints hello world', 1),
    (r'String url = "http://www.example.com"', 0),
    (r'//\\', 1),
    ('// "some comment"', 1),
    (r'new URI("http://www.google.com")', 0),
    (r'System.out.println("Escaped quote\""); // Comment', 1),
    ('hello world', 0),
    ('', 0),
    ("", 0),
])
def test_singleline_comments_zero_or_one(code_string, expected_count):
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count
