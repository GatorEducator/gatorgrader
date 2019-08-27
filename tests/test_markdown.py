"""Test cases for the markdown module."""

import pytest

from gator import markdown


@pytest.mark.parametrize(
    "writing_string,chosen_tag,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\n", "paragraph", 1),
        ("hello @world!!%^(@after)writing `a lot`.\n\nnew one", "code", 1),
        (
            "hello world!!%^(@after)writing a lot\n\n```\nblock\nof\ncode\n```\n",
            "code_block",
            1,
        ),
        ("hello world the fox is a code block", "code_block", 0),
        (
            "hello world!!%^(@after)writing a lot\n\n```\nblock\nof\ncode\n```\n",
            "code",
            0,
        ),
        (
            "hello world\n\n![Image](www.google.com)\n\n```\nblock\nof\ncode\n```\n",
            "image",
            1,
        ),
        (
            "hello world\n\n![Image](www.google.com)\n\n```\nblock\nof\ncode\n"
            "![Second Image](www.example.com)\nmore code\n```\n",
            "image",
            1,
        ),
    ],
)
def test_chosen_tag_zero_or_one(writing_string, chosen_tag, expected_count):
    """Check that it can detect one or more of a fragment."""
    assert markdown.count_specified_tag(writing_string, chosen_tag) == expected_count


@pytest.mark.parametrize(
    "writing_string,chosen_tag,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\n2nd paragraph", "paragraph", 2),
        (
            "# Section one\n\nparagraph of\ntext\n\n# Section two\n\nMore text\n",
            "heading",
            2,
        ),
        ("hello world the fox `code1` and `code3` and `code2`.", "code", 3),
        (
            "hello world `coding` !!%^(@after) ```mis-formatted code``` writing"
            "a lot\n\n```\nblock\nof\ncode\n```\n",
            "code_block",
            1,
        ),
        (
            "hello world\n\n![Image](www.google.com)\n\ntext and stuff\n"
            "![Second Image](www.example.com)\n",
            "image",
            2,
        ),
    ],
)
def test_chosen_tag_many(writing_string, chosen_tag, expected_count):
    """Check that it can detect many of a fragment."""
    assert markdown.count_specified_tag(writing_string, chosen_tag) == expected_count


def test_count_fragments_from_file(tmpdir):
    """Check that counting tags in a file works correctly."""
    test_contents = """
# Section One

Some text with `code`
in them.

#Section Two

With more `code blocks` and maybe an ![Image](www.example.com)."""

    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    hello_file.write(test_contents)
    assert hello_file.read() == test_contents
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.md"

    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 2
    assert exceeds_threshold is False

    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 1, hello_file, directory, False
    )
    assert actual_count == 2
    assert exceeds_threshold is True

    (exactly, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 1, hello_file, directory, True
    )
    assert actual_count == 2
    assert exactly is False

    (exactly, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 2, hello_file, directory, True
    )
    assert actual_count == 2
    assert exactly is True


def test_count_fragments_from_file_wildcard(tmpdir):
    """Check that counting tags in a file works correctly."""
    test_contents = """
# Section One

Some text with `code`
in them.

#Section Two

With more `code blocks` and maybe an ![Image](www.example.com)."""

    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    hello_file.write(test_contents)
    assert hello_file.read() == test_contents
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "*.md"

    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 2
    assert exceeds_threshold is False

    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 1, hello_file, directory, False
    )
    assert actual_count == 2
    assert exceeds_threshold is True

    (exactly, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 1, hello_file, directory, True
    )
    assert actual_count == 2
    assert exactly is False

    (exactly, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 2, hello_file, directory, True
    )
    assert actual_count == 2
    assert exactly is True


def test_count_fragments_from_empty_file(tmpdir):
    """Check that counting tags in a file works correctly if file is empty."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.md"
    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 0
    assert exceeds_threshold is False


def test_count_fragments_from_empty_file_wildcard(tmpdir):
    """Check that counting tags in a file works correctly if file is empty."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "*.md"
    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 0
    assert exceeds_threshold is False


def test_count_fragments_from_incorrect_file(tmpdir):
    """Check that counting tags in a file works correctly if file does not exist."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "HelloWrong.md"
    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 0
    assert exceeds_threshold is False


def test_count_fragments_from_incorrect_file_wildcard(tmpdir):
    """Check that counting tags in a file works correctly if file does not exist."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.md")
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Wrong*.md"
    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 0
    assert exceeds_threshold is False
    hello_file = "Wrong*.*"
    (exceeds_threshold, actual_count), count_dictionary = markdown.specified_tag_greater_than_count(
        "code", markdown.count_specified_tag, 3, hello_file, directory
    )
    assert actual_count == 0
    assert exceeds_threshold is False
