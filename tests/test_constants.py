"""Tests for the constants module"""

import pytest

from gator import constants


def test_language_constant_defined():
    """Check correctness for the variables in the language constant"""
    assert constants.languages.Python == "Python"
    assert constants.languages.Java == "Java"


def test_language_constant_cannot_redefine():
    """Check cannot redefine the variables in the language constant"""
    with pytest.raises(AttributeError):
        constants.languages.Java = "cannot_set_constant"
