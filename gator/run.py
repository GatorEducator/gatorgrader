"""Run a specified process"""

import subprocess
import sys

BLANK_LINE = "\n"
EMPTY = b""
NOTHING = ""
SPACE = " "


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
    # break up the output by newlines, discarding newlines
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
