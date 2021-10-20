"""Tests for the description module."""

import pytest

from gator import constants
from gator import description


class ArgParseWithDescription:
    """Mock class for ArgParse object containing a description."""

    def __init__(self, description):
        """Initialize mocked object with the given description."""
        self.description = description


class ArgParseWithNoDescription:
    """Mock class for ArgParse object not containing a description."""

    def __init__(self):
        """Initialize mocked object with a None description."""
        # An actual argparse object returns 'None' for anything
        # accessed via the "." operator that is not defined
        self.description = None


def test_get_description_argument_extracts_description():
    """Check that the description extraction function extracts the correct description."""
    desc = "A description"
    argparse = ArgParseWithDescription(desc)
    parsed_desc = description.get_description_argument(argparse)
    assert parsed_desc == desc


def test_get_description_argument_extracts_none():
    """Check that the description extraction function extracts None."""
    argparse = ArgParseWithNoDescription()
    parsed_desc = description.get_description_argument(argparse)
    assert parsed_desc is None


def test_transform_result_dictionary_transforms_with_description():
    """Check that the result transformation function adds the correct description."""
    desc = "A description"
    argparse = ArgParseWithDescription(desc)
    result_dict = {constants.results.Description: "something else"}
    result_dict = description.transform_result_dictionary(argparse, result_dict)
    assert result_dict[constants.results.Description] == desc


def test_transform_result_dictionary_transforms_with_no_description():
    """Check that the result transformation function does not modify the result dictionary."""
    argparse = ArgParseWithNoDescription()
    dict_desc = "something else"
    result_dict = {constants.results.Description: dict_desc}
    result_dict = description.transform_result_dictionary(argparse, result_dict)
    assert result_dict[constants.results.Description] == dict_desc


@pytest.mark.parametrize(
    "desc, expected_valid",
    [
        ("A description", True),
        ("A description with 'single' quotes", True),
        ("A description with 1 number.", True),
        ("A description with 1/2+4-2*5 math.", True),
        ("A description with @*&^%#1$?: symbols!", True),
        ('A description with escaped "double" quotes', False),
        ('A description with "double" quotes', False),
    ],
)
def test_is_valid_description(desc, expected_valid):
    """Check that the description validity function correctly detects if a description is valid."""
    is_valid = description.is_valid_description(desc)
    assert is_valid == expected_valid
