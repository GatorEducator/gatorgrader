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
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_comments_single(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = [
        "--directory",
        "D",
        "--file",
        "f",
        "--single",
        "2",
        "--language",
        "Java",
    ]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_comments_mult(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = [
        "--directory",
        "D",
        "--file",
        "f",
        "--multiple",
        "2",
        "--language",
        "Java",
    ]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_paragraphs(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--directory", "D", "--file", "f", "--paragraphs", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_words(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--directory", "D", "--file", "f", "--words", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_fragment_file(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = [
        "--directory",
        "D",
        "--file",
        "f",
        "--fragment",
        "GatorGrader",
        "--count",
        "2",
    ]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_count_file(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--directory", "D", "--file", "f", "--count", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_fragment_command(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "ls", "--fragment", "GatorGrader", "--count", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 7
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_count_command(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "ls", "--count", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 0


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_count_command_json(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue for JSON output"""
    chosen_arguments = ["--nowelcome", "--command", "ls", "--count", "2", "--json"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" not in captured.out
    assert counted_newlines == 2
    assert exit_code == 0


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_command(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "ls", "--executes"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 0


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_command_not_working(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "false", "--executes"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_command_working(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "true", "--executes"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 0


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_command_failing(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "true", "--count", "2"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 1


# pylint: disable=redefined-outer-name
# pylint: disable=bad-continuation
def test_perform_actions_display_welcome_and_ready_check_command_failing_exact(
    capsys, reset_results_dictionary
):
    """Check the argument verification, messages, and continue"""
    chosen_arguments = ["--command", "true", "--count", "2", "--exact"]
    exit_code = orchestrate.check(chosen_arguments)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 6
    assert exit_code == 1
