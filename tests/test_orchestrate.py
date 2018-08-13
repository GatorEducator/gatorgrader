"""Test cases for the orchestrate module"""

import pytest

from gator import orchestrate
from gator import report


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary"""
    report.reset()


def test_perform_actions_no_parameters_welcome(capsys):
    """Check to see if perform can invoke welcome action with no parameters"""
    actions = []
    actions.append([orchestrate.DISPLAY, "welcome_message", []])
    orchestrate.perform(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


def test_perform_actions_no_parameters_incorrect(capsys):
    """Check to see if perform can invoke welcome action with no parameters"""
    actions = []
    actions.append([orchestrate.DISPLAY, "incorrect_message", []])
    orchestrate.perform(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


# pylint: disable=unused-argument
def test_perform_actions_single_parameter_exit(capsys):
    """Check to see if perform can invoke exit actions with a parameter"""
    actions = []
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        actions.append([orchestrate.RUN, "run_exit", [orchestrate.INCORRECT_ARGUMENTS]])
        orchestrate.perform(actions)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_perform_actions_display_welcome_and_exit_check_arguments(capsys):
    """Check the argument verification, messages, and exit"""
    chosen_arguments = ["--directory", "D", "--file", "f"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        arguments, actions = orchestrate.check_arguments(chosen_arguments)
        assert arguments is not None
        orchestrate.perform(actions)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6


def test_perform_actions_display_welcome_and_exit_check(capsys):
    """Check the argument verification, messages, and exit"""
    chosen_arguments = ["--directory", "D", "--file", "f"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        orchestrate.check(chosen_arguments)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6


def test_perform_actions_display_welcome_and_ready_check_arguments(capsys):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--directory", "D", "--file", "f", "--exists"]
    arguments, actions = orchestrate.check_arguments(chosen_arguments)
    orchestrate.perform(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert arguments is not None
    assert "GatorGrader" in captured.out
    assert counted_newlines == 4


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_commit(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    # chosen_arguments = ["--directory", "D", "--file", "f", "--exists"]
    chosen_arguments = ["--commits", "33"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 0


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_exists(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--directory", "D", "--file", "f", "--exists"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 1
