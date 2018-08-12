"""Test cases for the orchestrate module"""

import pytest


from gator import orchestrate


# pylint: disable=unused-argument
def test_perform_actions_no_parameters_welcome(capsys):
    """Check to see if perform can invoke welcome action with no parameters"""
    actions = []
    actions.append([orchestrate.DISPLAY, "welcome_message", []])
    orchestrate.perform(actions)
    captured = capsys.readouterr()
    print(captured.out)
    counted_newlines = captured.out.count('\n')
    assert "GatorGrader" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


# pylint: disable=unused-argument
def test_perform_actions_no_parameters_incorrect(capsys):
    """Check to see if perform can invoke welcome action with no parameters"""
    actions = []
    actions.append([orchestrate.DISPLAY, "incorrect_message", []])
    orchestrate.perform(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count('\n')
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


# pylint: disable=unused-argument
def test_perform_actions_single_parameter_exit(capsys):
    """Check to see if perform can invoke exit actions with a parameter"""
    actions = []
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        actions.append([orchestrate.ORCHESTRATE, "exit", [orchestrate.INCORRECT_ARGUMENTS]])
        orchestrate.perform(actions)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == [2]
