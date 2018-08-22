"""Run a specified process"""

import subprocess
import sys

BLANK_LINE = "\n"
EMPTY = b""
NOTHING = ""
SPACE = " "


def specified_command_output_contains_fragment(command, expected_fragment):
    """Determines if the output is exactly equal to the count"""
    # run the command and gather the output and error details
    output, error = run_command(command)
    fragment_exists_output = 0
    # there was no error, so process output and check for fragment
    if error == EMPTY:
        actual_output = get_actual_output(output)
        fragment_exists_output = check_fragment_exists(expected_fragment, actual_output)
    return fragment_exists_output


def check_fragment_exists(expected_fragment, output_list):
    """Checks if a fragment exists in the list of output lines"""
    found_fragment = False
    for current_line in output_list:
        if expected_fragment in current_line:
            found_fragment = True
    return found_fragment


def specified_command_get_output(command):
    """Run the command and return the output as a String"""
    # run the command and gather the output and error details
    output, error = run_command(command)
    # there was no error, so process the output
    produced_output = NOTHING
    if error == EMPTY:
        actual_output = get_actual_output(output)
        produced_output = BLANK_LINE.join(actual_output)
    return produced_output


def get_actual_output(output):
    """Returns the actual lines from the command's output"""
    actual_output = []
    for line in output.splitlines(keepends=False):
        try:
            current_line_decoded = line.decode()
        except AttributeError:
            current_line_decoded = line
        actual_output.append(current_line_decoded)
    return actual_output


def run_command(command):
    """Run a command and return the output and error code"""
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    return output, error


def run_exit(exit_value):
    """Exit from the program using the provided exit value"""
    sys.exit(exit_value)
