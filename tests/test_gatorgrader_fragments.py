""""""

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
])
def test_singleline_comments_zero_or_one(writing_string, expected_count):
    assert gatorgrader_fragments.count_paragraphs(
        writing_string) == expected_count


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world!!%^(@after)writing a lot\n\nnew one', 2),
    ('hello world\n\nhi', 2),
    ('hello world\n\nhi\n\nff!$@name', 3),
    ('hello world\n\nhi\n\nff!$@name\n\n^^44', 4),
    ('hello world 44\n\nhi\n\nff!$@name\n\n^^44', 4),
])
def test_singleline_comments_many(writing_string, expected_count):
    assert gatorgrader_fragments.count_paragraphs(
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
    assert gatorgrader_fragments.count_specified_fragment(
        writing_string, chosen_fragment) == expected_count
