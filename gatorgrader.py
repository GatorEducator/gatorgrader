""" GatorGrader checks the files of programmers and writers """

import argparse
import os
import pytest
import sys

import gatorgrader_files
import gatorgrader_invoke


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


def display_welcome_message():
    """ Display a welcome message """
    print()
    print("GatorGrader: Automatically Check Files of Programmers and Writers")
    print("https://github.com/gkapfham/gatorgrader")
    print()


if __name__ == '__main__':
    display_welcome_message()
    # parse and verify the arguments
    print(sys.argv[1:])
    gg_arguments = parse_gatorgrader_arguments(sys.argv[1:])
    did_verify_arguments = verify_gatorgrader_arguments(gg_arguments)
    if did_verify_arguments is False:
        print("Incorrect command-line arguments.")
        sys.exit(2)
    else:
        print("Valid command-line arguments.")
        print("Running the specified checks!")
        # CHECK: all of the files exist in their directories
        if gg_arguments.directories is not None and gg_arguments.checkfiles is not None:
            gatorgrader_invoke.invoke_all_file_in_directory_checks(
                gg_arguments.checkfiles, gg_arguments.directories)
