""" test cases for the gatorgrader_utils module """

import os
import pytest

import gatorgrader_comments


def test_file_contains_singleline_comment(tmpdir):
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write('//// hello world')
    assert hello_file.read() == "//// hello world"
    assert len(tmpdir.listdir()) == 1
    print()
    print("tmpdir:", tmpdir)
    print("hello_file bn:", hello_file.basename)
    print("type of hello_file:", type(hello_file))
    comment_count = gatorgrader_comments.count_entities(
        hello_file.basename,
        hello_file.dirname,
        gatorgrader_comments.count_singleline_java_comment)
    assert comment_count == 1


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
    (' ', 0),
    (" ", 0),
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
    ('System.out.println("Hello, World!\n"); // prints hello world \n //hello',
     2),
    ('// hello \n System.out.println("Hello, World!\n"); \n //hello', 2),
    ('String url = "http://www.example.com"; \n //hello', 1),
    ('//\\ \n //hi', 2),
    ('// "some comment"', 1),
    ('new URI("http://www.google.com") \n // hi', 1),
    ('\n // hi \n //hi', 2),
])
def test_singleline_comments_many(code_string, expected_count):
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count


@pytest.mark.parametrize("code_string,expected_count", [
    ('/* hello world */', 1),
    ('/** hello world */', 1),
    ('/* hello */ \n world', 1),
    ('/* hello */ world', 1),
    ('/** hello */ \n world', 1),
    ('/** hello */ world', 1),
    ('/** hello **/ world', 1),
    ('/* hello world */ && --', 1),
    ('/* hello world  */ __ --', 1),
    ('/** hello world **/ && --', 1),
    ('/** hello world  **/ __ --', 1),
    ('/* hello world', 0),
    ('/ hello world', 0),
    (' hello world', 0),
    ('// hello world', 0),
    ('/ hello world', 0),
    (' ', 0),
    (" ", 0),
    ('', 0),
    ("", 0),
])
def test_multiline_comments_zero_or_one(code_string, expected_count):
    assert gatorgrader_comments.count_multiline_java_comment(
        code_string) == expected_count


@pytest.mark.parametrize("code_string,expected_count", [
    ('/* hello world */ \n /* hello world */', 2),
    ('/* hello */ \n world \n /* hello world */', 2),
    ('/* hello */ world \n /* hello world */', 2),
    ('/** hello world */ \n /* hello world */', 2),
    ('/** hello */ \n world \n /* hello world */', 2),
    ('/** hello @author me */ world \n /* hello world */', 2),
    ('/** hello @author me **/ world \n /* hello world */', 2),
])
def test_multiline_comments_zero_or_one(code_string, expected_count):
    assert gatorgrader_comments.count_multiline_java_comment(
        code_string) == expected_count


@pytest.mark.parametrize("code_string,expected_count", [
    ('// hello world /** hello */', 1),
    ('// hello world /** hello */ \n /** hello */', 2),
    ('// hello world hello ', 0),
    ('/** hi */ \n /** hi again */', 2),
    ('/** hi */ \n // whoa /** hi again */', 2),
])
def test_multiline_comments_mixed(code_string, expected_count):
    assert gatorgrader_comments.count_multiline_java_comment(
        code_string) == expected_count


@pytest.mark.parametrize("code_string,expected_count", [
    ('// hello world /** hello */', 1),
    ('// hello world /** hello */ \n /** hello */', 1),
    ('/** hi */ \n // hello world hello ', 1),
    ('/** hi */ \n // hello world hello \n // hi again', 2),
])
def test_singleline_comments_mixed(code_string, expected_count):
    assert gatorgrader_comments.count_singleline_java_comment(
        code_string) == expected_count
