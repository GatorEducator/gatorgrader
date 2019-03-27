"""Test cases for the comments and entities modules"""

import pytest

from gator import comments
from gator import entities


def test_file_contains_singleline_java_comment_count(tmpdir):
    """Checks that the singleline comment count works"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("//// hello world")
    assert hello_file.read() == "//// hello world"
    assert len(tmpdir.listdir()) == 1
    comment_count = entities.count_entities(
        hello_file.basename, hello_file.dirname, comments.count_singleline_java_comment
    )
    assert comment_count == 1


def test_file_contains_multiline_java_comment_count(tmpdir):
    """Checks that the multiline comment count works"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    comment_count = entities.count_entities(
        hello_file.basename, hello_file.dirname, comments.count_multiline_java_comment
    )
    assert comment_count == 1


def test_file_contains_multiline_python_comment_count(tmpdir):
    """Checks that the multiline python comment count works"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    string = "Hello \n World"
    hello_file.write('"""{}"""'.format(string))
    assert hello_file.read() == '"""Hello \n World"""'
    assert len(tmpdir.listdir()) == 1
    comment_count = entities.count_entities(
        hello_file.basename, hello_file.dirname, comments.count_multiline_python_comment
    )
    assert comment_count == 1


def test_file_contains_singleline_comment_greater(tmpdir):
    """Checks that the file is above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("//// hello world")
    assert hello_file.read() == "//// hello world"
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_singleline_java_comment,
    )
    assert greater_than_count is True


def test_file_contains_multiline_comment_greater(tmpdir):
    """Checks that the file is above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_multiline_java_comment,
    )
    assert greater_than_count is True


def test_file_contains_multiline_python_comment_greater(tmpdir):
    """Checks that the file is above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    string = "Hello \n World"
    hello_file.write('"""{}"""'.format(string))
    assert hello_file.read() == '"""Hello \n World"""'
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_multiline_python_comment,
    )
    assert greater_than_count is True

def test_file_contains_singleline_comment_not_greater(tmpdir):
    """Checks that the file is not above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/ hello world")
    assert hello_file.read() == "/ hello world"
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_singleline_java_comment,
    )
    assert greater_than_count is False


def test_file_contains_multiline_comment_not_greater(tmpdir):
    """Checks that the file is not above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/ hello world")
    assert hello_file.read() == "/ hello world"
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_multiline_java_comment,
    )
    assert greater_than_count is False


def test_file_contains_multiline_python_comment_not_greater(tmpdir):
    """Checks that the file is not above the check level"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.py")
    string = "Hello \n World"
    hello_file.write('"""{}"""'.format(string))
    assert hello_file.read() == '"""Hello \n World"""'
    assert len(tmpdir.listdir()) == 1
    greater_than_count, _ = entities.entity_greater_than_count(
        hello_file.basename,
        hello_file.dirname,
        1,
        comments.count_multiline_java_comment,
    )
    assert greater_than_count is False


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("//// hello world", 1),
        ("//// hello // world", 1),
        ("//// hello //// world", 1),
        ("// hello world ff", 1),
        ("// hello world && --", 1),
        ("// hello world  __ --", 1),
        ('System.out.println("Hello, World!\n"); // prints hello world', 1),
        ('String url = "http://www.example.com"', 0),
        (r"//\\", 1),
        ('// "some comment"', 1),
        ('new URI("http://www.google.com")', 0),
        (r'System.out.println("Escaped quote\""); // Comment', 1),
        ("hello world", 0),
        ("", 0),
        ("", 0),
        (" ", 0),
        (" ", 0),
    ],
)
def test_singleline_comments_zero_or_one(code_string, expected_count):
    """Check that it finds zero or one single-line comments"""
    assert comments.count_singleline_java_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("# hello world", 1),
        ("# hello # world", 1),
        ("# hello //// world", 1),
        ("# hello world ff", 1),
        ("# hello world && --", 1),
        ("# hello world  __ --", 1),
        ('print("Hello, World!\n"); # prints hello world', 1),
        ('String url = "http://www.example.com"', 0),
        (r"#\\", 1),
        ('# "some comment"', 1),
        ('new URI("http://www.google.com")', 0),
        (r'System.out.println("Escaped quote\""); # Comment', 1),
        ("hello world", 0),
        ("", 0),
        ("", 0),
        (" ", 0),
        (" ", 0),
    ],
)
def test_singleline_comments_zero_or_one_python(code_string, expected_count):
    """Checks that it finds zero or one Python comments"""
    assert comments.count_singleline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("// hello world \n//hello world", 2),
        ("// hello world \n//hello world\n//hello world", 3),
        ("//// hello world\n//hello", 2),
        ("//// hello // world\n//hello", 2),
        ("//// hello //// world\n//hello\n", 2),
        ("// hello world\n //hello", 2),
        ("// hello world && --\n//hello", 2),
        ("// hello world  __ --\n//hello", 2),
        ('System.out.println("Hello, World!\n"); // prints hello world \n //hello', 2),
        ('// hello \n System.out.println("Hello, World!\n"); \n //hello', 2),
        ('String url = "http://www.example.com"; \n //hello', 1),
        ("//\\ \n //hi", 2),
        ('// "some comment"', 1),
        ('new URI("http://www.google.com") \n // hi', 1),
        ("\n // hi \n //hi", 2),
    ],
)
def test_singleline_comments_many(code_string, expected_count):
    """Checks that it finds many singleline comments"""
    assert comments.count_singleline_java_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("# hello world \n#hello world", 2),
        ("# hello world \n#hello world\n#hello world", 3),
        ("### hello world\n##hello", 2),
        ("#### hello ## world\n##hello", 2),
        ("### hello # world\n##hello\n", 2),
        ("# hello world\n #hello", 2),
        ("# hello world && --\n #hello", 2),
        ("# hello world  __ --\n#hello", 2),
        ('print("Hello, World!\n"); # prints hello world \n #hello', 2),
        ('# hello \n System.out.println("Hello, World!\n"); \n #hello', 2),
        ('String url = "http://www.example.com"; \n #hello', 1),
        ("#h \n #hi", 2),
        ('# "some comment"', 1),
        ('new URI("http://www.google.com") \n # hi', 1),
        ("\n # hi \n #hi", 2),
    ],
)
def test_singleline_comments_many_python(code_string, expected_count):
    """Checks that it finds many singleline comments"""
    assert comments.count_singleline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("/* hello world */", 1),
        ("/** hello world */", 1),
        ("/* hello */ \n world", 1),
        ("/* hello */ world", 1),
        ("/** hello */ \n world", 1),
        ("/** hello */ world", 1),
        ("/** hello **/ world", 1),
        ("/* hello world */ && --", 1),
        ("/* hello world  */ __ --", 1),
        ("/** hello world **/ && --", 1),
        ("/** hello world  **/ __ --", 1),
        ("/* hello world", 0),
        ("/ hello world", 0),
        (" hello world", 0),
        ("// hello world", 0),
        ("/ hello world", 0),
        (" ", 0),
        (" ", 0),
        ("", 0),
        ("", 0),
    ],
)
def test_multiline_comments_zero_or_one(code_string, expected_count):
    """Checks that it finds zero or one multiline comments"""
    assert comments.count_multiline_java_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ('""" hello \n world"""', 1),
        ('"""hello\n world\n"""', 1),
        ('"""\nhello world\n"""', 1),
        ('"""\nhello\n world\n"""', 1),
        ('"""\nhello world\n', 0),
        ('""\nhello world\n""', 0),
        ('""" hello world\n"""', 1),
        ('""""""', 1),
        ('""" """', 1),
        ('""" hello world', 0),
        ('""hello world""', 0),
        ('"hello world"', 0),
        ("# hello world", 0),
        ("## hello world", 0),
        ('# hello world\n"""', 0),
        ('"""# hello\n world', 0),
        (" hello world", 0),
        ('"hello world"', 0),
        (" ", 0),
        ("", 0),
    ],
)
def test_multiline_python_comments_zero_or_one(code_string, expected_count):
    """Checks that it finds zero or one multiline comments"""
    assert comments.count_multiline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("/* hello world */ \n /* hello world */", 2),
        ("/* hello */ \n world \n /* hello world */", 2),
        ("/* hello */ world \n /* hello world */", 2),
        ("/** hello world */ \n /* hello world */", 2),
        ("/** hello */ \n world \n /* hello world */", 2),
        ("/** hello @author me */ world \n /* hello world */", 2),
        ("/** hello @author me **/ world \n /* hello world */", 2),
    ],
)
def test_multiline_comments_two(code_string, expected_count):
    """Checks that it has two or more multiline python comments"""
    assert comments.count_multiline_java_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ('""" hello world """ \n """ hello world """', 2),
        ('""" hello """ \n world \n """ hello world """', 2),
        ('""" hello """ \n """ hello world """', 2),
        ('""" hello world """ \n """ hello \n world """', 2),
        ('""" hello """ \n world \n """ hello world """', 2),
        ('""" hello @author me """ \n """ hello world """', 2),
        ('""" hello\n@author me """\n world \n """ hello world """', 2),
    ],
)
def test_multiline_python_comments_two(code_string, expected_count):
    """Checks that it has two or more multiline python comments"""
    assert comments.count_multiline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("// hello world /** hello */", 1),
        ("// hello world /** hello */ \n /** hello */", 2),
        ("// hello world hello ", 0),
        ("/** hi */ \n /** hi again */", 2),
        ("/** hi */ \n // whoa /** hi again */", 2),
    ],
)
def test_multiline_comments_mixed(code_string, expected_count):
    """Checks that it can find multiline comments in mixtures"""
    assert comments.count_multiline_java_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("# hello world" + '"""hello \n """', 1),
        ("# hello world" + '"""hello \n """' + '"""hello \n """', 2),
        ('""" hello world hello ', 0),
        ('"""hello \n """' + '"""hello \n world"""', 2),
        ('""" hi \n"""' + "\n # whoa " + '""" hi \n again """', 2),
    ],
)
def test_multiline_python_comments_mixed(code_string, expected_count):
    """Checks that it can find multiline comments in mixtures"""
    assert comments.count_multiline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("// hello world /** hello */", 1),
        ("// hello world /** hello */ \n /** hello */", 1),
        ("/** hi */ \n // hello world hello ", 1),
        ("/** hi */ \n // hello world hello \n // hi again", 2),
    ],
)
def test_singleline_comments_mixed(code_string, expected_count):
    """Checks that it can find singleline comments in mixtures"""
    assert comments.count_singleline_java_comment(code_string) == expected_count

@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("hello world", 0),
        ('""" hello world """ """ hello world """', 0),
        ('\n """hello world"""', 0),
        ('"""hello \n world"""', 1),
        ('"""hello \n world"""'+"hello world", 1),
        ('""" hello \n world """ \n """ hello world """', 1),
    ],
)
def test_multiline_docstring_comments_zero_or_one_python(code_string, expected_count):
    """Checks that it finds zero or one multiline Python docstring comments"""
    assert comments.count_multiline_python_comment(code_string) == expected_count


@pytest.mark.parametrize(
    "code_string,expected_count",
    [
        ("# hello world" + '"""hello \n """', 1),
        ("# hello world" + '"""hello \n """' + '"""hello \n """', 2),
        ('""" hello world hello ', 0),
        ('"""hello \n """' + '"""hello \n world"""', 2),
        ('""" hi \n"""' + "\n # whoa " + '""" hi \n again """', 2),
        ('"""hello \n """' + '"""hello \n world"""' + '"""hello \n world hello"""', 3),
        ('"""hello \n """' + '"""hello \n world"""' + '"""hello \n world hello"""' + '"""hello world \n ** hello"""', 4),
        ('"""hello \n """' + '"""hello \n world"""' + '"""hello \n world hello"""' + '"""hello world \n ** hello"""' + '"""hello world $$$ \n world hello"""', 5)
    ],
)
def test_multiline_docstring_comments_many_python(code_string, expected_count):
    """Checks that it finds many multiline Python docstring comments"""
    assert comments.count_multiline_python_comment(code_string) == expected_count
