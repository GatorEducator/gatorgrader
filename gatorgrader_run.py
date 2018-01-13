""" Functions that run a specified process """

import subprocess

BLANK_LINE = "\n"


def specified_command_output_equals_count(command, expected_count):
    """Determines if the output is exactly equal to the count"""
    output, error = run_command(command)
    actual_output = get_actual_output(output)
    actual_line_count = count_output_lines(actual_output)
    if expected_count == actual_line_count:
        return True
    return False


def count_output_lines(output):
    """ Counts the lines of program output """
    return len(output)


def specified_command_output_contains_fragment(command, expected_fragment):
    """Determines if the output is exactly equal to the count"""
    output, error = run_command(command)
    actual_output = get_actual_output(output)
    fragment_exists_output = check_fragment_exists(expected_fragment,
                                                   actual_output)
    return fragment_exists_output


def check_fragment_exists(expected_fragment, output_list):
    """Checks if a fragment exists in the list of output lines"""
    found_fragment = False
    for current_line in output_list:
        if expected_fragment in current_line:
            found_fragment = True
    return found_fragment


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
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error
