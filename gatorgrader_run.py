""" Functions that run a specified process """

import subprocess

BLANK_LINE = "\n"
JAVA = "Java"
TASK_MARKER = ":run"


def specified_command_output_equals_count(command, expected_count, language):
    """ Determines if the output is exactly equal to the count """
    output, error = run_command(command)
    if language == JAVA:
        actual_output = get_actual_java_output(output)
    else:
        actual_output = get_actual_output(output)
    actual_line_count = count_outpupt_lines(actual_output)
    if expected_count == actual_line_count:
        return True
    return False


def count_outpupt_lines(output):
    """ Counts the lines of program output """
    return len(output)


def get_actual_java_output(output):
    """ Returns the actual lines from the command's output """
    actual_output = []
    capture_output = False
    for line in output.splitlines(keepends=True):
        try:
            line = line.decode()
        except AttributeError:
            pass
        if BLANK_LINE == line:
            capture_output = False
        if capture_output is True:
            actual_output.append(line)
        if TASK_MARKER in line:
            capture_output = True
    return actual_output

def get_actual_output(output):
    """ Returns the actual lines from the command's output """
    actual_output = []
    for line in output.splitlines(keepends=False):
        actual_output.append(line)
    return actual_output


def run_command(command):
    """ Run a command and return the output and error code """
    print("Running command: ", command)
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error
