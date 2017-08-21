""" Functions that run a specified process """

import subprocess


TASK_MARKER = "Task :run"
BLANK_LINE = "\n"


def get_actual_java_output(output):
    """ Returns the actual lines from the command's output """
    actual_output = []
    capture_output = False
    print("output: ", output)
    for line in output.splitlines(keepends=True):
        print("line: ", line)
        if BLANK_LINE == line:
            capture_output = False
        if capture_output is True:
            actual_output.append(line)
        if TASK_MARKER in line:
            capture_output = True
    return actual_output


def run_command(command):
    """ Run a command and return the output and error code """
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error
