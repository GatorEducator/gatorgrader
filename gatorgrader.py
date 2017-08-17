#!/usr/bin/env python3

""" GatorGrader checks the files of programmers and writers """

import os
import sys

import argparse

import gatorgrader_invoke

SLASH = "/"
GATORGRADER_HOME = "GATORGRADER_HOME"


def parse_gatorgrader_arguments(args):
    """ Parses the arguments provided on the command-line """
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    gg_parser.add_argument('--checkfiles', nargs='+', type=str)
    gg_parser.add_argument('--directories', nargs='+', type=str)

    gg_arguments = gg_parser.parse_args(args)
    return gg_arguments


def verify_gatorgrader_arguments(args):
    """ Checks if the arguments are correct """
    verified_arguments = True
    if args.checkfiles is not None and args.directories is None:
        verified_arguments = False
    elif args.directories is not None and args.checkfiles is None:
        verified_arguments = False
    elif args.directories is not None and args.checkfiles is not None:
        if len(args.directories) != len(args.checkfiles):
            verified_arguments = False
    return verified_arguments


def verify_gatorgrader_home(current_gatorgrader_home):
    """ Verifies that the GATORGRADER_HOME environment variable is set correctly """
    verified_gatorgrader_home = False
    if current_gatorgrader_home is not None and current_gatorgrader_home.endswith(
            SLASH) is True:
        verified_gatorgrader_home = True
    return verified_gatorgrader_home


def get_gatorgrader_home():
    """ Returns the GATORGRADER_HOME """
    current_gatorgrader_home = os.environ.get(GATORGRADER_HOME)
    had_to_set = False
    # the current gatorgrader_home is acceptable, so use it
    if verify_gatorgrader_home(current_gatorgrader_home) is not False:
        gatorgrader_home = current_gatorgrader_home
    # the current gatorgrader_home is not okay, so guess at one
    else:
        gatorgrader_home = os.getcwd() + SLASH
        had_to_set = True
    return gatorgrader_home, had_to_set


def display_welcome_message():
    """ Display a welcome message """
    print()
    print(
        "GatorGrader: Automatically Check the Files of Programmers and Writers"
    )
    print("https://github.com/gkapfham/gatorgrader")
    print()


if __name__ == '__main__':
    display_welcome_message()
    # parse and verify the arguments
    gg_arguments = parse_gatorgrader_arguments(sys.argv[1:])
    did_verify_arguments = verify_gatorgrader_arguments(gg_arguments)
    if did_verify_arguments is False:
        print("Incorrect command-line arguments.")
        sys.exit(2)
    else:
        print("Valid command-line arguments.")
        print("Running the specified checks!")
        print()
        # CHECK: all of the files exist in their directories
        if gg_arguments.directories is not None and gg_arguments.checkfiles is not None:
            gatorgrader_invoke.invoke_all_file_in_directory_checks(
                gg_arguments.checkfiles, gg_arguments.directories)
