"""Testing to see if GatorGrader can check for correct fragments"""

import pytest

import gatorgrader_fragments


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world', 1),
    ('hello world!!%^()', 1),
    ('hello world!!%^(@after)', 1),
    ('hello world!!%^(@after)writing a lot', 1),
    ('hello world!!%^(@after)writing a lot\n', 1),
    ('hello world!!%^(@after)writing a lot\n\n', 1),
    ('', 0),
    ("", 0),
    (' ', 0),
    (" ", 0),
    ("     ", 0),
    ('     ', 0),
    ('a     ', 1),
    ("a     ", 1),
    ("a\n     ", 1),
    ('# Section Header', 0),
    ('# Section Header\n\nNot Section Header', 1),
    ('Paragraph\n\n\n# Section Header', 1),
    ('Paragraph\n\n```\nShould not be a paragraph\n```', 1),
    ('```\nShould not be\na paragraph\n```', 0),
    ('Beginning of paragraph ``` Still in fences but now \
    also in paragraph ``` and end', 1),
])
def test_paragraphs_zero_or_one(writing_string, expected_count):
    """Check that it can detect zero or one paragraphs"""
    assert gatorgrader_fragments.count_paragraphs(
        writing_string) == expected_count


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world!!%^(@after)writing a lot\n\nnew one', 2),
    ('hello world\n\nhi', 2),
    ('hello world\n\nhi\n\nff!$@name', 3),
    ('hello world\n\nhi\n\nff!$@name\n\n^^44', 4),
    ('hello world 44\n\nhi\n\nff!$@name\n\n^^44', 4),
    ('# Section Header\n\nhello world 44\n\nhi\n\nff!$@name\n\n^^44', 4),
])
def test_paragraphs_many(writing_string, expected_count):
    """Check that it can detect two or more paragraphs"""
    assert gatorgrader_fragments.count_paragraphs(
        writing_string) == expected_count


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world! Writing a lot.\n\nnew one.', 1),
    ('hello world! Writing a lot.\n\nNew one. Question?', 2),
    ('The method test.main was called. Hello world! Writing a lot.\n\n'
     'New one. Question? Fun!', 3),
    ('The method test.main was called. Hello world! Writing a lot.\n\n'
     'New one. Question? Fun! Nice!', 3),
    ('The method test.main was called. Hello world! Example? Writing.\n\n'
     'New one. Question? Fun! Nice!', 4),
    ('The method test.main was called.\nHello world! Example? Writing.\n\n'
     'New one. Question? Fun! Nice!', 4),
    ('Here is one paragraph.\nIt should end up having three sentences. '
     'Here is the third sentence\n\n```\nHere\'s a correctly formatted code'
     ' block that should not be considered as a paragraph to count sentences'
     ' in.\n```\n\nAnd now here is the second paragraph. It will also '
     'have three sentences. The third is a short one.', 3),
])
def test_sentences_different_counts(writing_string, expected_count):
    """Check that it can detect different counts of sentences"""
    assert gatorgrader_fragments.count_sentences(
        writing_string) == expected_count


@pytest.mark.parametrize("writing_string,chosen_fragment,expected_count", [
    ('hello world!!%^(@after)writing a lot\n\nnew one', 'writing', 1),
    ('hello @world!!%^(@after)writing a lot\n\nnew one', '@world', 1),
    ('hello world!!%^(@after)writing a lot\n\nnew one', '@world', 0),
    ('System.out.println(new Date())', 'new Date()', 1),
    ('System.out.println(new Date())', 'new Date', 1),
])
def test_chosen_fragment_zero_or_one(writing_string, chosen_fragment,
                                     expected_count):
    """Check that it can detect one or more of a fragment"""
    assert gatorgrader_fragments.count_specified_fragment(
        writing_string, chosen_fragment) == expected_count


@pytest.mark.parametrize("writing_string,chosen_fragment,expected_count", [
    ('hello world!!%^(@after)writing a lot\n\nnew one writing', 'writing', 2),
    ('hello @world!!%^(@after)writing a lot\n\nnew new new one', 'new', 3),
    ('hello @world!!%^(@after)writing a @world lot\n\nnew one', '@world', 2),
    ('System.out.println(new Date()) \n new Date()', 'new Date()', 2),
    ('System.out.println(new Date() new Date() new Date())', 'new Date', 3),
])
def test_chosen_fragment_many(writing_string, chosen_fragment,
                              expected_count):
    """Check that it can detect many of a fragment"""
    assert gatorgrader_fragments.count_specified_fragment(
        writing_string, chosen_fragment) == expected_count
