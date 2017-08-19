""""""

import pytest

import gatorgrader_fragments


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world', 1),
    ('', 0),
    ("", 0),
    # (' ', 0),
    # (" ", 0),
])
def test_singleline_comments_zero_or_one(writing_string, expected_count):
    assert gatorgrader_fragments.count_paragraphs(
        writing_string) == expected_count


@pytest.mark.parametrize("writing_string,expected_count", [
    ('hello world\n\nhi', 2),
    ('hello world\n\nhi\n\nff!$@name', 3),
    ('hello world\n\nhi\n\nff!$@name\n\n^^44', 4),
    ('hello world 44\n\nhi\n\nff!$@name\n\n^^44', 4),
])
def test_singleline_comments_many(writing_string, expected_count):
    assert gatorgrader_fragments.count_paragraphs(
        writing_string) == expected_count
