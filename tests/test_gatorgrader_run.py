""" test cases for the gatorgrader_run module """

import gatorgrader_run


def test_run_command_returns_ls():
    """Checks that a single line is returned from command """
    output, error = gatorgrader_run.run_command("echo \"Hello!\"")
    assert error == b''
    assert output == b'Hello!\n'


def test_capture_output_actual():
    """Checks that the count is correct"""
    sample_output = "\n\n> Task :run\nGregory M. Kapfhammer Mon Aug 21 15:08:38 EDT 2017\nHello world.\nGradle is great.\nTravis is tremendous.\n\nBUILD SUCCESSFUL in 0s\n2 actionable tasks: 1 executed, 1 up-to-date"
    actual_output = gatorgrader_run.get_actual_java_output(sample_output)
    assert len(actual_output) == 4


def test_capture_output_actual_count():
    """Checks that the count is correct"""
    sample_output = "\n\n> Task :run\nGregory M. Kapfhammer Mon Aug 21 15:08:38 EDT 2017\nHello world.\nGradle is great.\nTravis is tremendous.\n\nBUILD SUCCESSFUL in 0s\n2 actionable tasks: 1 executed, 1 up-to-date"
    actual_output = gatorgrader_run.get_actual_java_output(sample_output)
    assert gatorgrader_run.count_output_lines(actual_output) == len(
        actual_output)
