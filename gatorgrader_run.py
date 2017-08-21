""" Functions that run a specified process """

import subprocess


def run_command(command):
    """ Run a command and return the output and error code """
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error
