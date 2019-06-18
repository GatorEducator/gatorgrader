"""Test cases for the fragments module.."""

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
        # headers
        ("# Section Header", 0),
        ("# Section Header\n\nNot Section Header", 1),
        ("Paragraph\n\n\n# Section Header", 1),
        # lists
        ("Paragraph1\n - first item\n - second item", 1),
        (" - first item\n - second item\n", 0),
        # code blocks
        ("Paragraph\n\n```\nShould not be a paragraph\n```", 1),
        ("```\nShould not be\na paragraph\n```", 0),
        ("Paragraph `inline code block` and end", 1),
    ],
)
def test_paragraphs_zero_or_one(writing_string, expected_count):
    """Check that it can detect zero or one paragraphs."""
    assert fragments.count_paragraphs(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("hello world!!%^(@after)writing a lot\n\nnew one", 2),
        ("hello world\n\nhi", 2),
        ("hello world\n\nhi\n\nff!$@name", 3),
        ("hello world\n\nhi\n\nff!$@name\n\n^^44", 4),
        ("hello world 44\n\nhi\n\nff!$@name\n\n^^44", 4),
        # headers
        ("# Section Header\n\nhello world 44\n\nhi\n\nff!$@name\n\n^^44", 4),
        # lists
        ("Paragraph1\n 1. item one\n 2. item two\n\nParagraph2", 2),
        # Thematic, line and soft breaks
        ("** ***", 0),
        ("This is one paragraph.\n___\nThis is another paragraph.", 2),
        ("Line break.  \nHello\\\nLine break.", 1),
        ("This is a soft break\n\nThis is the second paragraph", 2),
    ],
)
def test_paragraphs_many(writing_string, expected_count):
    """Check that it can detect two or more paragraphs."""
    assert fragments.count_paragraphs(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count, expected_paragraph_count",
    [
        ("", 0, 0),
        ("hello world! Writing a lot.\n\nsingle.", 1, 2),
        ("hello world! Writing a lot.\n\nnew one.", 2, 2),
        ("hello world! Writing a lot.\n\nNew one. Question?", 3, 2),
        ("This should be `five` words", 5, 1),
        ("This should still be `six` word's", 6, 1),
        ("The command `pipenv run pytest` should test", 7, 1),
        (
            "The method test.main was called. Hello world! Writing a lot.\n\n"
            "New one. Question? Fun!",
            4, 2
        ),
        (
            "New one. Question? Fun! Nice!\n\n"
            "The method test.main was called. Hello world! Writing a lot.",
            5, 2
        ),
        (
            "The method `test.main` was called. Hello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            5, 2
        ),
        (
            "The method test.main was called.\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            5, 2
        ),
        # code blocks
        (
            "Here is some code in a code block.\n\n```\ndef test_function():\n    "
            "function_call()\n```\n\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            4, 3
        ),
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. `Code?` Question? Fun! Nice!",
            6, 2
        ),
        # images
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. [Image](https://example.com/image.png) Question? Fun! Nice!",
            6, 2
        ),
        # links
        ("[This link is five words](www.url.com)", 5, 1),
        # emoji
        (":thumbsup: is an emoji", 4, 1),
        # new lines
        ("One sentence is\nanother's problem.", 5, 1),
        ("One sentence's\ngreat delusion.", 4, 1),
    ],
)
def test_words_different_min_counts(writing_string, expected_count, expected_paragraph_count):
    """Check that it can detect different counts of words."""
    # only check the minimum count
    # note that the default summarization function in a minimum
    actual_count, actual_count_dictionary = fragments.count_words(writing_string)
    assert actual_count == expected_count
    assert len(actual_count_dictionary) == expected_paragraph_count
    actual_count, actual_count_dictionary = fragments.count_words(writing_string, min)
    assert len(actual_count_dictionary) == expected_paragraph_count
    assert actual_count == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("", 0),
        ("hello world! Writing a lot.\n\nsingle.", 1),
        ("hello world! Writing a lot.\n\nnew one.", 2),
        ("hello world! Writing a lot.\n\nNew one. Question?", 3),
        ("This should be `five` words", 5),
        ("This should still be `six` word's", 6),
        ("The command `pipenv run pytest` should test", 7),
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
        # code blocks
        (
            "Here is some code in a code block.\n\n```\ndef test_function():\n    "
            "function_call()\n```\n\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            4,
        ),
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. `Code?` Question? Fun! Nice!",
            6,
        ),
        # images
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. [Image](https://example.com/image.png) Question? Fun! Nice!",
            6,
        ),
        # links
        ("[This link is five words](www.url.com)", 5),
        # emoji
        (":thumbsup: is an emoji", 4),
        # new lines
        ("One sentence is\nanother's problem.", 5),
        ("One sentence's\ngreat delusion.", 4),
    ],
)
def test_minimum_words_different_min_counts(writing_string, expected_count):
    """Check that it can detect different counts of words."""
    # only check the minimum count
    assert fragments.count_minimum_words(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("", 0),
        ("hello world! Writing a lot.\n\nsingle.", 6),
        ("hello world! Writing a lot.\n\nnew one.", 7),
        ("hello world! Writing a lot.\n\nNew one. Question?", 8),
        ("This should be `five` words", 5),
        ("This should still be `six` word's", 6),
        ("The command `pipenv run pytest` should test", 7),
        (
            "The method test.main was called. Hello world! Writing a lot.\n\n"
            "New one. Question? Fun!",
            15,
        ),
        (
            "New one. Question? Fun! Nice!\n\n"
            "The method test.main was called. Hello world! Writing a lot.",
            16,
        ),
        (
            "The method `test.main` was called. Hello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            15,
        ),
        (
            "The method test.main was called.\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            15,
        ),
        # code blocks
        (
            "Here is some code in a code block.\n\n```\ndef test_function():\n    "
            "function_call()\n```\n\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            17,
        ),
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. `Code?` Question? Fun! Nice!",
            21,
        ),
        # images
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. [Image](https://example.com/image.png) Question? Fun! Nice!",
            21,
        ),
        # links
        ("[This link is five words](www.url.com)", 5),
        # emoji
        (":thumbsup: is an emoji", 4),
        # new lines
        ("One sentence is\nanother's problem.", 5),
        ("One sentence's\ngreat delusion.", 4),
    ],
)
def test_total_words_different_sum_counts(writing_string, expected_count):
    """Check that it can detect different counts of total words."""
    # only check the sum count
    assert fragments.count_total_words(writing_string) == expected_count


@pytest.mark.parametrize(
    "writing_string,expected_count",
    [
        ("", 0),
        ("hello world! Writing a lot.\n\nsingle.", 6),
        ("hello world! Writing a lot.\n\nnew one.", 7),
        ("hello world! Writing a lot.\n\nNew one. Question?", 8),
        ("This should be `five` words", 5),
        ("This should still be `six` word's", 6),
        ("The command `pipenv run pytest` should test", 7),
        (
            "The method test.main was called. Hello world! Writing a lot.\n\n"
            "New one. Question? Fun!",
            15,
        ),
        (
            "New one. Question? Fun! Nice!\n\n"
            "The method test.main was called. Hello world! Writing a lot.",
            16,
        ),
        (
            "The method `test.main` was called. Hello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            15,
        ),
        (
            "The method test.main was called.\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            15,
        ),
        # code blocks
        (
            "Here is some code in a code block.\n\n```\ndef test_function():\n    "
            "function_call()\n```\n\nHello world! Example? Writing.\n\n"
            "New one. Question? Fun! Nice!",
            17,
        ),
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. `Code?` Question? Fun! Nice!",
            21,
        ),
        # images
        (
            "Here is some code in an inline code block: `def test_function():`. "
            "Hello world! Example? Writing.\n\n"
            "New one. [Image](https://example.com/image.png) Question? Fun! Nice!",
            21,
        ),
        # links
        ("[This link is five words](www.url.com)", 5),
        # emoji
        (":thumbsup: is an emoji", 4),
        # new lines
        ("One sentence is\nanother's problem.", 5),
        ("One sentence's\ngreat delusion.", 4),
    ],
)
def test_words_different_sum_counts(writing_string, expected_count):
    """Check that it can detect different counts of total words."""
    # only check the sum count
    assert fragments.count_words(writing_string, sum) == expected_count


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
    """Check that it can detect one or more of a fragment."""
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
    """Check that it can detect many of a fragment."""
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
    """Create some strings and then see if breaking them up in lines works."""
    line_list = fragments.get_line_list(writing_string)
    assert len(line_list) == expected_count


def test_count_entities_from_file(tmpdir):
    """Check that counting fragments in a file works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_entities(
        "hello", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 1
    count = fragments.count_entities(
        "world", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 1
    count = fragments.count_entities(
        "planet", fragments.count_specified_fragment, hello_file, directory, ""
    )
    assert count == 0


def test_count_entities_from_contents():
    """Check that counting fragments in a string works correctly."""
    value = "/* hello world */"
    count = fragments.count_entities(
        "hello", fragments.count_specified_fragment, contents=value
    )
    assert count == 1
    count = fragments.count_entities(
        "world", fragments.count_specified_fragment, contents=value
    )
    assert count == 1
    count = fragments.count_entities(
        "planet", fragments.count_specified_fragment, contents=value
    )
    assert count == 0


def test_count_entities_from_file_with_threshold(tmpdir):
    """Check that counting fragments in a file with threshold works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        "hello", fragments.count_specified_fragment, 10, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        "hello", fragments.count_specified_fragment, 1, hello_file, directory, ""
    )
    assert actual_count == 1
    assert exceeds_threshold is True


def test_count_entities_from_contents_with_threshold():
    """Check that counting fragments with threshold in a string works correctly."""
    value = "/* hello world */"
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        "hello", fragments.count_specified_fragment, 10, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        "hello", fragments.count_specified_fragment, 1, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is True


def test_count_single_line_from_file(tmpdir):
    """Check that counting lines in a file works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("/* hello world */")
    assert hello_file.read() == "/* hello world */"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_lines(hello_file, directory, "")
    assert count == 1


def test_count_single_line_from_contents():
    """Check that counting lines in contents works correctly."""
    hello_contents = "Hello.java"
    count = fragments.count_lines("", "", hello_contents)
    assert count == 1


def test_count_single_line_from_file_with_threshold(tmpdir):
    """Check that counting lines in a file with threshold works correctly."""
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
    """Check that counting lines in a file works correctly."""
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
    """Check that counting lines in a file works correctly."""
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
    """Check that counting lines in contents works correctly with blanks."""
    hello_contents = (
        '/* hello world */\nString s = new String("hello");\n\n//this is a comment'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_single_blank():
    """Check that counting lines in contents works correctly."""
    hello_contents = (
        '/* hello world */\nString s = new String("hello");\n//this is a comment'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_multiple_blanks():
    """Check that counting lines in contents works correctly."""
    hello_contents = (
        '/* hello world */\n\nString s = new String("hello");\n//this is a comment\n\n'
    )
    count = fragments.count_lines("", "", hello_contents)
    assert count == 3


def test_count_multiple_lines_from_contents_with_threshold():
    """Check that counting lines in contents works correctly."""
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
    """Create some strings and then see blank detection for the line works."""
    found_blanks = fragments.is_blank_line(writing_string)
    assert found_blanks == expected_status


@pytest.mark.parametrize(
    "regex,expected_status",
    [
        (r"<footer>([^;]*)\<\/footer>", True),
        (r"\\begin([^;]*)\\end", True),
        (r"bibliography", True),
        (r"section", True),
        (r"[^]", False),
        (r"[)", False),
    ],
)
def test_is_valid_regex(regex, expected_status):
    """Check that regex assessment correctly validates regular expressions."""
    is_valid = fragments.is_valid_regex(regex)
    assert is_valid == expected_status


@pytest.mark.parametrize(
    "writing_string,chosen_regex,expected_count",
    [
        (
            "\\begin{abstract}\nThis is the paper's abstract\n\\end{abstract}",
            r"\\begin(.*?)\\end",
            1,
        ),
        (
            "\\begin{enumerate}\n\\item hi\n\\item bye\n\\end{enumerate}"
            "\nsome random string",
            r"\\begin(.*?)\\end",
            1,
        ),
        ("\\begin{document}the document never ends", r"\\begin(.*?)\\end", 0),
        ("\\bibliographystyle{abbrv}\n\\bibliography{main}", r"\\begin(.*?)\\end", 0),
        (
            "\\bibliographystyle{abbrv}\n\\bibliography{main}\ninvalid",
            r"\\begin\{.*?\}",
            0,
        ),
        ("<footer>this nice foot</footer>", r"<footer>(.*?)<\/footer>", 1),
    ],
)
def test_chosen_regex_zero_or_one(writing_string, chosen_regex, expected_count):
    """Check that it can detect one or more of a regex."""
    assert (
        fragments.count_specified_regex(writing_string, chosen_regex) == expected_count
    )


@pytest.mark.parametrize(
    "writing_string,chosen_regex,expected_count",
    [
        (
            "\\begin{abstract} hello\\end{abstract} \\begin{enumerate} world\\end{enumerate}",
            r"\\begin(.*?)\\end",
            2,
        ),
        (
            "\\begin{enumerate}\\item1 \\end{enumerate} \\begin{enumerate}\\item2"
            "\\end{enumerate} \\begin{enumerate}\\item3 \\end{enumerate}",
            r"\\begin(.*?)\\end",
            3,
        ),
        (
            "<footer>happiness</footer> <footer>everything</footer>",
            r"<footer>(.*?)<\/footer>",
            2,
        ),
        (
            "<footer>happiness</footer> <footer>everything</footer>",
            r"<footer>(.*)<\/footer>",
            1,
        ),
        ("\\begin{thing1} \\begin \\begin{main}invalid", r"\\begin\{itemize\}", 0),
    ],
)
def test_chosen_regex_many(writing_string, chosen_regex, expected_count):
    """Check that it can detect many of a regex."""
    assert (
        fragments.count_specified_regex(writing_string, chosen_regex) == expected_count
    )


def test_count_regex_from_file(tmpdir):
    """Check that counting regex in a file works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("\\begin{document} hello! \\end{document}")
    assert hello_file.read() == "\\begin{document} hello! \\end{document}"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    count = fragments.count_entities(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, hello_file, directory
    )
    assert count == 1
    count = fragments.count_entities(
        r"planet", fragments.count_specified_regex, hello_file, directory, ""
    )
    assert count == 0
    count = fragments.count_entities(
        r"invalid[^]", fragments.count_specified_regex, hello_file, directory, ""
    )
    assert count == -1


def test_count_regex_from_contents():
    """Check that counting regex in a string works correctly."""
    value = "\\begin{document} hello! \\end{document}"
    count = fragments.count_entities(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, contents=value
    )
    assert count == 1
    count = fragments.count_entities(
        r"planet", fragments.count_specified_regex, contents=value
    )
    assert count == 0
    count = fragments.count_entities(
        r"invalid[^]", fragments.count_specified_regex, contents=value
    )
    assert count == -1


def test_count_regex_from_file_with_threshold(tmpdir):
    """Check that counting regex in a file with threshold works correctly."""
    hello_file = tmpdir.mkdir("subdirectory").join("Hello.java")
    hello_file.write("\\begin{document} hello! \\end{document}")
    assert hello_file.read() == "\\begin{document} hello! \\end{document}"
    assert len(tmpdir.listdir()) == 1
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "subdirectory"
    hello_file = "Hello.java"
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, 2, hello_file, directory
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, 1, hello_file, directory
    )
    assert actual_count == 1
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"invalid[^]", fragments.count_specified_regex, 0, hello_file, directory
    )

    assert actual_count == -1
    assert exceeds_threshold is False


def test_count_regex_from_contents_with_threshold():
    """Check that counting regex with threshold in a string works correctly."""
    value = "\\begin{document} hello! \\end{document}"
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, 10, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is False
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"\\begin(.*?)\\end", fragments.count_specified_regex, 1, contents=value
    )
    assert actual_count == 1
    assert exceeds_threshold is True
    exceeds_threshold, actual_count = fragments.specified_entity_greater_than_count(
        r"invalid[^]", fragments.count_specified_regex, 0, contents=value
    )
    assert actual_count == -1
    assert exceeds_threshold is False
