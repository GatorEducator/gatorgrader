"""Tests for the constants module."""

import pytest

from gator import constants

CANNOT_SET_CONSTANT_VARIABLE = "cannot_set_constant_variable"


def test_languages_constant_defined():
    """Check correctness for the variables in the languages constant."""
    assert constants.languages.Python == "Python"
    assert constants.languages.Java == "Java"


def test_markers_constant_defined():
    """Check correctness for the variables in the markers constant."""
    assert constants.markers.Empty == b""
    assert constants.markers.Newline == "\n"
    assert constants.markers.No_Diagnostic == ""
    assert constants.markers.Nothing == ""
    assert constants.markers.Space == " "
    assert constants.markers.Invalid == -1


def test_paths_constant_defined():
    """Check correctness for the variables in the paths constant."""
    assert constants.paths.Current_Directory == "."
    assert constants.paths.Current_Directory_Glob == "*.*"
    assert constants.paths.Home == "gatorgrader"


def test_markdown_constant_defined():
    """Check correctness for the variables in the markdown constant."""
    assert constants.markdown.Paragraph == "paragraph"
    assert constants.markdown.Softbreak == "softbreak"


def test_codes_constant_defined():
    """Check correctness for the variables in the codes constant."""
    assert constants.codes.Error == 1
    assert constants.codes.Success == 0


def test_arguments_constant_defined():
    """Check correctness for the variables in the arguments constant."""
    assert constants.arguments.Incorrect == 2
    assert constants.arguments.Void == []


def test_modules_constant_defined():
    """Check correctness for the variables in the modules constant."""
    assert constants.modules.Display == "gator.display"
    assert constants.modules.Invoke == "gator.invoke"
    assert constants.modules.Report == "gator.report"
    assert constants.modules.Run == "gator.run"


def test_outputs_constant_defined():
    """Check correctness for the variables in the outputs constant."""
    assert constants.outputs.Json == "JSON"
    assert constants.outputs.Text == "TEXT"


def test_results_constant_defined():
    """Check correctness for the variables in the results constant."""
    assert constants.results.Check == "check"
    assert constants.results.Outcome == "outcome"
    assert constants.results.Diagnostic == "diagnostic"


def test_versioncontrol_constant_defined():
    """Check correctness for the variables in the versioncontrol constant."""
    assert constants.versioncontrol.Master == "master"


def test_words_constant_defined():
    """Check correctness for the variables in the versioncontrol constant."""
    assert constants.words.Minimum == "word(s) in every paragraph"
    assert constants.words.Total == "word(s) in total"


def test_environmentvariables_constant_defined():
    """Check correctness for the variables in the environmentvariables constant."""
    assert constants.environmentvariables.Home == "GATORGRADER_HOME"


def test_languages_constant_cannot_redefine():
    """Check cannot redefine the variables in the languages constant."""
    with pytest.raises(AttributeError):
        constants.languages.Java = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.languages.Python = CANNOT_SET_CONSTANT_VARIABLE


def test_markers_constant_cannot_redefine():
    """Check cannot redefine the variables in the markers constant."""
    with pytest.raises(AttributeError):
        constants.markers.Arrow = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Empty = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Newline = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.No_Diagnostic = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Nothing = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Space = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Tab = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Invalid = 10


def test_paths_constant_cannot_redefine():
    """Check cannot redefine the variables in the paths constant."""
    with pytest.raises(AttributeError):
        constants.paths.Current_Directory = CANNOT_SET_CONSTANT_VARIABLE
        constants.paths.Current_Directory_Glob = CANNOT_SET_CONSTANT_VARIABLE
        constants.paths.Home = CANNOT_SET_CONSTANT_VARIABLE


def test_markdown_constant_cannot_redefine():
    """Check cannot redefine the variables in the markdown constant."""
    with pytest.raises(AttributeError):
        constants.markdown.Paragraph = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markdown.Softbreak = CANNOT_SET_CONSTANT_VARIABLE


def test_codes_constant_cannot_redefine():
    """Check cannot redefine the variables in the codes constant."""
    with pytest.raises(AttributeError):
        constants.codes.Success = 10
    with pytest.raises(AttributeError):
        constants.codes.Error = 10


def test_arguments_constant_cannot_redefine():
    """Check cannot redefine the variables in the arguments constant."""
    with pytest.raises(AttributeError):
        constants.arguments.Incorrect = 100
    with pytest.raises(AttributeError):
        constants.codes.Void = [100]


def test_modules_constant_cannot_redefine():
    """Check cannot redefine the variables in the paths constant."""
    with pytest.raises(AttributeError):
        constants.modules.Display = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.modules.Invoke = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.modules.Report = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.modules.Run = CANNOT_SET_CONSTANT_VARIABLE


def test_outputs_constant_cannot_redefine():
    """Check cannot redefine the variables in the outputs constant."""
    with pytest.raises(AttributeError):
        constants.outputs.Json = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.outputs.Text = CANNOT_SET_CONSTANT_VARIABLE


def test_results_constant_cannot_redefine():
    """Check cannot redefine the variables in the results constant."""
    with pytest.raises(AttributeError):
        constants.results.Check = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.results.Outcome = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.results.Diagnostic = CANNOT_SET_CONSTANT_VARIABLE


def test_versioncontrol_constant_cannot_redefine():
    """Check cannot redefine the variables in the versioncontrol constant."""
    with pytest.raises(AttributeError):
        constants.versioncontrol.Master = CANNOT_SET_CONSTANT_VARIABLE


def test_words_constant_cannot_redefine():
    """Check cannot redefine the variables in the words constant."""
    with pytest.raises(AttributeError):
        constants.words.Minimum = CANNOT_SET_CONSTANT_VARIABLE
        constants.words.Total = CANNOT_SET_CONSTANT_VARIABLE


def test_environmentvariables_constant_cannot_redefine():
    """Check cannot redefine the variables in the environmentvariables constant."""
    with pytest.raises(AttributeError):
        constants.environmentvariables.Home = CANNOT_SET_CONSTANT_VARIABLE
