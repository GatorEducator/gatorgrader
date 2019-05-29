"""Tests for the constants module"""

import pytest

from gator import constants


def test_language_constant_defined():
    """Check correctness for the variables in the language constant"""
    assert constants.languages.Python == "Python"
    assert constants.languages.Java == "Java"


def test_marker_constant_defined():
    """Check correctness for the variables in the marker constant"""
    assert constants.markers.Empty == b""
    assert constants.markers.Newline == "\n"
    assert constants.markers.No_Diagnostic == ""
    assert constants.markers.Nothing == ""
    assert constants.markers.Space == " "
    assert constants.markers.Success == 0


def test_paths_constant_defined():
    """Check correctness for the variables in the paths constant"""
    assert constants.paths.Current_Directory_Glob == "*.*"


def test_language_constant_cannot_redefine():
    """Check cannot redefine the variables in the languages constant"""
    with pytest.raises(AttributeError):
        constants.languages.Java = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.languages.Python = "cannot_set_constant"


def test_marker_constant_cannot_redefine():
    """Check cannot redefine the variables in the markers constant"""
    with pytest.raises(AttributeError):
        constants.markers.Empty = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markers.Newline = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markers.No_Diagnostic = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markers.Nothing = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markers.Space = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markers.Success = 10


def test_paths_constant_cannot_redefine():
    """Check cannot redefine the variables in the paths constant"""
    with pytest.raises(AttributeError):
        constants.paths.Current_Directory_Glob = "cannot_set_constant"
