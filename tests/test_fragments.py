"""Test cases for the fragments module"""

import pytest

from gator import fragments


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("hello world", 1),
        ("hello world!!%^()", 1),
        ("hello world!!%^(@after)", 1),
        ("hello world!!%^(@after)writing a lot", 1),
        ("hello world!!%^(@after)writing a lot\n", 1),
        ("hello world!!%^(@after)writing a lot\n\n", 1),
        ("", 0),
        (" ", 0),
        ("     ", 0),
        ("a     ", 1),
        ("a\n     ", 1),
        ("# Section Header", 0),
        ("# Section Header\n\nNot Section Header", 1),
        ("Paragraph\n\n\n# Section Header", 1),
        ("Paragraph\n\n```\nShould not be a paragraph\n```", 1),
        ("```\nShould not be\na paragraph\n```", 0),
        ("Paragraph `inline code block` and end", 1),
    ],
)
def test_paragraphs_zero_or_one(writing_string, expected_count):
    """Check that it can detect zero or one paragraphs"""
    assert fragments.count_paragraphs(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\nnew one", 2),
        ("hello world\n\nhi", 2),
        ("hello world\n\nhi\n\nff!$@name", 3),
        ("hello world\n\nhi\n\nff!$@name\n\n^^44", 4),
        ("hello world 44\n\nhi\n\nff!$@name\n\n^^44", 4),
        ("# Section Header\n\nhello world 44\n\nhi\n\nff!$@name\n\n^^44", 4),
    ],
)
def test_paragraphs_many(writing_string, expected_count):
    """Check that it can detect two or more paragraphs"""
    assert fragments.count_paragraphs(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("hello world! Writing a lot.\n\nsingle.", 1),
        ("hello world! Writing a lot.\n\nnew one.", 2),
        ("hello world! Writing a lot.\n\nNew one. Question?", 3),
        (
            "The method test.main was called. Hello world! Writing a lot.\n\n"
            "New one. Question? Fun!",
            4,
        ),
        (
            "New one. Question? Fun! Nice!\n\n"
            "The method test.main was called. Hello world! Writing a lot.",
            5,
        ),
        (
            "The method `test.main` was called. Hello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            5,
        ),
        (
            "The method test.main was called.\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            5,
        ),
        (
            "Here is some code in a code block.\n\n```\ndef test_function():\n    "
            "function_call()\n```\n\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            4,
        ),
        ("", 0),
    ],
)
def test_words_different_counts(writing_string, expected_count):
    """Check that it can detect different counts of words"""
    assert fragments.count_words(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,chosen_fragment,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\nnew one", "writing", 1),
        ("hello @world!!%^(@after)writing a lot\n\nnew one", "@world", 1),
        ("hello world!!%^(@after)writing a lot\n\nnew one", "@world", 0),
        ("System.out.println(new Date())", "new Date()", 1),
        ("System.out.println(new Date())", "new Date", 1),
    ],
)
def test_chosen_fragment_zero_or_one(writing_string, chosen_fragment, expected_count):
    """Check that it can detect one or more of a fragment"""
    assert (
        fragments.count_specified_fragment(writing_string, chosen_fragment)
        == expected_count
    )


@pytest.mark.parametrize(
    "writing_string,chosen_fragment,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\nnew one writing", "writing", 2),
        ("hello @world!!%^(@after)writing a lot\n\nnew new new one", "new", 3),
        ("hello @world!!%^(@after)writing a @world lot\n\nnew one", "@world", 2),
        ("System.out.println(new Date()) \n new Date()", "new Date()", 2),
        ("System.out.println(new Date() new Date() new Date())", "new Date", 3),
    ],
)
def test_chosen_fragment_many(writing_string, chosen_fragment, expected_count):
    """Check that it can detect many of a fragment"""
    assert (
        fragments.count_specified_fragment(writing_string, chosen_fragment)
        == expected_count
    )


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("System.out.println(new Date() new Date() new Date())", 1),
        ("hello world!!%^(@after)writing a lot\nnew one writing", 2),
        ("hello @world!!%^(@after)writing a @world lot\nnew one", 2),
        ("System.out.println(new Date()) \nnew Date()", 2),
        ("hello @world!!%^(@after)writing a lot\nnew new new one\nthird one", 3),
        ("hello @world!!%^(@after)writing a lot\nnew new new one\nthird one\n\n", 3),
    ],
)
def test_extract_line_list(writing_string, expected_count):
    """Create some strings and then see if breaking them up in lines works"""
    line_list = fragments.get_line_list(writing_string)
    assert len(line_list) == expected_count


def test_count_fragments_from_file(tmpdir):
    """Checks that counting fragments in a file works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_fragments(
        "hello", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 1
    count = fragments.count_fragments(
        "world", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 1
    count = fragments.count_fragments(
        "planet", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 0


def test_count_fragments_from_contents():
    """Checks that counting fragments in a string works correctly"""
    value = "/* hello world */"
    count = fragments.count_fragments(
        "hello", fragments.count_specified_fragment, contents=value
    )
    assert count == 1
    count = fragments.count_fragments(
        "world", fragments.count_specified_fragment, contents=value
    )
    assert count == 1
    count = fragments.count_fragments(
        "planet", fragments.count_specified_fragment, contents=value
    )
    assert count == 0


def test_count_fragments_from_file_with_threshold(tmpdir):
    """Checks that counting fragments in a file with threshold works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    exceeds_threshold, actual_count = fragments.specified_fragment_greater_than_count(
        "hello", fragments.count_specified_fragment, 10, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_fragment_greater_than_count(
        "hello", fragments.count_specified_fragment, 1, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is True


def test_count_fragments_from_contents_with_threshold():
    """Checks that counting fragments with threshold in a string works correctly"""
    value = "/* hello world */"
    exceeds_threshold, actual_count = fragments.specified_fragment_greater_than_count(
        "hello", fragments.count_specified_fragment, 10, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_fragment_greater_than_count(
        "hello", fragments.count_specified_fragment, 1, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is True


def test_count_single_line_from_file(tmpdir):
    """Checks that counting lines in a file works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_lines(hello_file, directory, "")
    assert count == 1


def test_count_single_line_from_contents():
    """Checks that counting lines in contents works correctly"""
    hello_contents = "Hello.java"
    count = fragments.count_lines("", "", hello_contents)
    assert count == 1


def test_count_single_line_from_file_with_threshold(tmpdir):
    """Checks that counting lines in a file with threshold works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        1, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        100, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is False


def test_count_multiple_lines_from_file(tmpdir):
    """Checks that counting lines in a file works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write(
        '/* hello world */\nString s = new String("hello");\n//this is a comment'
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_lines(hello_file, directory, "")
    assert count == 3


def test_count_multiple_lines_from_file_with_threshold(tmpdir):
    """Checks that counting lines in a file works correctly"""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write(
        '/* hello world */\nString s = new String("hello");\n//this is a comment'
    )
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        2, hello_file, directory, ""
    )
    assert actual_count == 3
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        3, hello_file, directory, ""
    )
    assert actual_count == 3
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        100, hello_file, directory, ""
    )
    assert actual_count == 3
    assert exceeds_threshold is False


def test_count_multiple_lines_from_contents():
    """Checks that counting lines in contents works correctly with blanks"""
    hello_contents = (
        '/* hello world */\nString s = new String("hello");\n\n//this is a comment'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_single_blank():
    """Checks that counting lines in contents works correctly"""
    hello_contents = (
        '/* hello world */\nString s = new String("hello");\n//this is a comment'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_multiple_blanks():
    """Checks that counting lines in contents works correctly"""
    hello_contents = (
        '/* hello world */\n\nString s = new String("hello");\n//this is a comment\n\n'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_with_threshold():
    """Checks that counting lines in contents works correctly"""
    hello_contents = (
        '/* hello world */\nString s = new String("hello");\n//this is a comment'
    )
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        2, "", "", hello_contents
    )
    assert actual_count == 3
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        3, "", "", hello_contents
    )
    assert actual_count == 3
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_source_greater_than_count(
        100, "", "", hello_contents
    )
    assert actual_count == 3
    assert exceeds_threshold is False


@pytest.mark.parametrize(
    "writing_string,expected_status",
    [
        (None, True),
        ("", True),
        ("\n", True),
        ("\n\n", True),
        ("\n \n", True),
        ("\t", True),
        ("\t \t", True),
        ("\n \t", True),
        ("\t \n", True),
        ("     ", True),
        ("  \t   ", True),
        ("  \n   ", True),
        ("  \t  \n   ", True),
        ("  \n  \t   ", True),
        ("System.out.println(new Date() new Date() new Date())", False),
        (
            "hello @world!!%^(@after)writing a lot\nnew new new one\nthird one\n\n",
            False,
        ),
    ],
)
def test_detect_blank_line(writing_string, expected_status):
    """Create some strings and then see blank detection for the line works"""
    found_blanks = fragments.is_blank_line(writing_string)
    assert found_blanks == expected_status
