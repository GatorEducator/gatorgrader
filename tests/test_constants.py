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
    assert constants.markers.Invalid == -1


def test_paths_constant_defined():
    """Check correctness for the variables in the paths constant"""
    assert constants.paths.Current_Directory_Glob == "*.*"


def test_markdown_constant_defined():
    """Check correctness for the variables in the paragraphs constant"""
    assert constants.markdown.Paragraph == "paragraph"
    assert constants.markdown.Softbreak == "softbreak"


def test_codes_constant_defined():
    """Check correctness for the variables in the codes constant"""
    assert constants.codes.Error == 1
    assert constants.codes.Success == 0


def test_arguments_constant_defined():
    """Check correctness for the variables in the arguments constant"""
    assert constants.arguments.Incorrect == 2
    assert constants.arguments.Void == []


def test_modules_constant_defined():
    """Check correctness for the variables in the modules constant"""
    assert constants.modules.Display == "gator.display"
    assert constants.modules.Invoke == "gator.invoke"
    assert constants.modules.Report == "gator.report"
    assert constants.modules.Run == "gator.run"


def test_output_constant_defined():
    """Check correctness for the variables in the output constant"""
    assert constants.output.Json == "JSON"
    assert constants.output.Text == "TEXT"


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
        constants.markers.Invalid = 10


def test_paths_constant_cannot_redefine():
    """Check cannot redefine the variables in the paths constant"""
    with pytest.raises(AttributeError):
        constants.paths.Current_Directory_Glob = "cannot_set_constant"


def test_markdown_constant_cannot_redefine():
    """Check cannot redefine the variables in the markdown constant"""
    with pytest.raises(AttributeError):
        constants.markdown.Paragraph = "cannot_set_constant"
    with pytest.raises(AttributeError):
        constants.markdown.Softbreak = "cannot_set_constant"


def test_codes_constant_cannot_redefine():
    """Check cannot redefine the variables in the codes constant"""
    with pytest.raises(AttributeError):
        constants.codes.Success = 10
    with pytest.raises(AttributeError):
        constants.codes.Error = 10


def test_arguments_constant_cannot_redefine():
    """Check cannot redefine the variables in the arguments constant"""
    with pytest.raises(AttributeError):
        constants.arguments.Incorrect = 100
    with pytest.raises(AttributeError):
        constants.codes.Void = [100]


def test_modules_constant_cannot_redefine():
    """Check cannot redefine the variables in the paths constant"""
    with pytest.raises(AttributeError):
        constants.modules.Display = "cannot_redefine"
    with pytest.raises(AttributeError):
        constants.modules.Invoke = "cannot_redefine"
    with pytest.raises(AttributeError):
        constants.modules.Report = "cannot_redefine"
    with pytest.raises(AttributeError):
        constants.modules.Run = "cannot_redefine"


def test_outputs_constant_cannot_redefine():
    """Check cannot redefine the variables in the outputs constant"""
    with pytest.raises(AttributeError):
        constants.output.Json = "cannot_redefine"
    with pytest.raises(AttributeError):
        constants.output.Text = "cannot_redefine"
