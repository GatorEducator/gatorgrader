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
    ('System.out.println("Hello, World!\n"); // prints hello world', 1),
    ('String url = "http://www.example.com"', 0),
    (r'//\\', 1),
    ('// "some comment"', 1),
    ('new URI("http://www.google.com")', 0),
    (r'System.out.println("Escaped quote\""); // Comment', 1),
    ('hello world', 0),
    ('', 0),
    ("", 0),
])
def test_singleline_comments_zero_or_one(code_string, expected_count):
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count


@pytest.mark.parametrize("code_string,expected_count", [
    ('// hello world \n//hello world', 2),
    ('// hello world \n//hello world\n//hello world', 3),
    ('//// hello world\n//hello', 2),
    ('//// hello // world\n//hello', 2),
    ('//// hello //// world\n//hello\n', 2),
    ('// hello world\n //hello', 2),
    ('// hello world && --\n//hello', 2),
    ('// hello world  __ --\n//hello', 2),
    ('System.out.println("Hello, World!\n"); // prints hello world \n //hello', 2),
    ('// hello \n System.out.println("Hello, World!\n"); \n //hello', 2),
    ('String url = "http://www.example.com"; \n //hello', 1),
    ('//\\ \n //hi', 2),
    ('// "some comment"', 1),
    ('new URI("http://www.google.com") \n // hi', 1),
    ('\n // hi \n //hi', 2),
])
def test_singleline_comments_many(code_string, expected_count):
    print(code_string)
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count
