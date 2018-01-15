"""GatorGrader checks the files of programmers and writers"""

import os
import sys

import argparse

import gatorgrader_invoke
import gatorgrader_exit

SLASH = "/"
GATORGRADER_HOME = "GATORGRADER_HOME"

DEFAULT_COUNT = 0
DEFAULT_LANGUAGE = "Java"
INCORRECT_ARGUMENTS = 2
JAVA = "Java"
PYTHON = "Python"

SINGLE = "single-line"
MULTIPLE = "multiple-line"

REPOSITORY = "."


def parse_gatorgrader_arguments(args):
    """Parses the arguments provided on the command-line"""
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    gg_parser.add_argument(
        "--nowelcome",
        help="Do not display the welcome message",
        action="store_true")

    gg_parser.add_argument('--checkfiles', nargs='+', type=str)
    gg_parser.add_argument('--directories', nargs='+', type=str)

    gg_parser.add_argument('--singlecomments', nargs='+', type=int)

    gg_parser.add_argument('--multicomments', nargs='+', type=int)

    gg_parser.add_argument('--paragraphs', nargs='+', type=int)
    gg_parser.add_argument('--sentences', nargs='+', type=int)

    gg_parser.add_argument('--fragments', nargs='+', type=str)
    gg_parser.add_argument('--fragmentcounts', nargs='+', type=int)

    gg_parser.add_argument('--languages', nargs="+", type=str)

    gg_parser.add_argument('--commands', nargs='+', type=str)
    gg_parser.add_argument('--outputlines', nargs='+', type=int)

    gg_parser.add_argument('--commits', type=int)

    gg_arguments_finished = gg_parser.parse_args(args)
    return gg_arguments_finished


def verify_gatorgrader_arguments(args):
    """Checks if the arguments are correct"""
    verified_arguments = True
    # TODO: This verification is not complete and/or incorrect
    if args.checkfiles is not None and args.directories is None:
        verified_arguments = False
    elif args.directories is not None and args.checkfiles is None:
        verified_arguments = False
    elif args.directories is not None and args.checkfiles is not None:
        if len(args.directories) != len(args.checkfiles):
            verified_arguments = False
    elif args.singlecomments is not None:
        if args.checkfiles is None or args.directories is None:
            verified_arguments = False
    elif args.multicomments is not None:
        if args.checkfiles is None or args.directories is None:
            verified_arguments = False
    elif args.paragraphs is not None:
        if args.checkfiles is None or args.directories is None:
            verified_arguments = False
    elif args.sentences is not None:
        if args.checkfiles is None or args.directories is None:
            verified_arguments = False
    elif args.fragments is None and args.fragmentcounts is not None:
        verified_arguments = False
    return verified_arguments


def verify_gatorgrader_home(current_gatorgrader_home):
    """Verifies that the GATORGRADER_HOME variable is set correctly"""
    verified_gatorgrader_home = False
    if (current_gatorgrader_home is not None
            and current_gatorgrader_home.endswith(SLASH) is True):
        verified_gatorgrader_home = True
    return verified_gatorgrader_home


def get_gatorgrader_home():
    """Returns the GATORGRADER_HOME"""
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
    """Display a welcome message"""
    print()
    print(
        "GatorGrader: Automatically Check the Files of Programmers and Writers"
    )
    print("https://github.com/gkapfham/gatorgrader")
    print()


def display_checking_message():
    """Display the checking message"""
    print("Valid command-line arguments.")
    print("Running the specified checks!")
    print()


if __name__ == '__main__':
    # parse and verify the arguments
    gg_arguments = parse_gatorgrader_arguments(sys.argv[1:])
    did_verify_arguments = verify_gatorgrader_arguments(gg_arguments)
    # incorrect arguments, exit program
    if did_verify_arguments is False:
        print("Incorrect command-line arguments.")
        sys.exit(INCORRECT_ARGUMENTS)
    # correct arguments, so perform the checks
    else:
        if gg_arguments.nowelcome is not True:
            display_welcome_message()
            display_checking_message()
        check_return_values = []
        # CHECK: all of the files exist in their directories
        if (gg_arguments.directories is not None
                and gg_arguments.checkfiles is not None):
            current_invoke_return_values =\
                gatorgrader_invoke.invoke_all_file_in_directory_checks(
                    gg_arguments.checkfiles, gg_arguments.directories)
            check_return_values.extend(current_invoke_return_values)
            # CHECK: Java code contains 'k' single-line comments
            if gg_arguments.singlecomments is not None:
                current_invoke_return_values =\
                    gatorgrader_invoke.invoke_all_comment_checks(
                        gg_arguments.checkfiles, gg_arguments.directories,
                        gg_arguments.singlecomments, SINGLE,
                        gg_arguments.languages)
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Java code contains 'k' multiple-line comments
            if gg_arguments.multicomments is not None:
                current_invoke_return_values =\
                    gatorgrader_invoke.invoke_all_comment_checks(
                        gg_arguments.checkfiles, gg_arguments.directories,
                        gg_arguments.multicomments, MULTIPLE,
                        gg_arguments.languages)
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Writing contains 'k' paragraphs
            if gg_arguments.paragraphs is not None:
                current_invoke_return_values =\
                    gatorgrader_invoke.invoke_all_paragraph_checks(
                        gg_arguments.checkfiles, gg_arguments.directories,
                        gg_arguments.paragraphs)
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Writing all paragraphs contain 'k' sentences
            if gg_arguments.sentences is not None:
                current_invoke_return_values =\
                    gatorgrader_invoke.invoke_all_sentence_checks(
                        gg_arguments.checkfiles, gg_arguments.directories,
                        gg_arguments.sentences)
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Content contains 'k' specified fragments
            if (gg_arguments.fragments is not None and
                    gg_arguments.fragmentcounts is not None):
                current_invoke_return_values =\
                    gatorgrader_invoke.invoke_all_fragment_checks(
                        gg_arguments.checkfiles, gg_arguments.directories,
                        gg_arguments.fragments, gg_arguments.fragmentcounts)
                check_return_values.extend(current_invoke_return_values)
        # CHECK: Command produces 'k' lines of output
        elif (gg_arguments.commands is not None
              and gg_arguments.outputlines is not None):
            current_invoke_return_values =\
                gatorgrader_invoke.invoke_all_command_checks(
                    gg_arguments.commands, gg_arguments.outputlines)
            check_return_values.extend(current_invoke_return_values)
        # CHECK: Command produces lines of output with the specified fragment
        elif (gg_arguments.commands is not None
              and gg_arguments.fragments is not None):
            current_invoke_return_values =\
                gatorgrader_invoke.invoke_all_command_fragment_checks(
                    gg_arguments.commands, gg_arguments.fragments)
            check_return_values.extend(current_invoke_return_values)
        # CHECK: Repository contains at least 'k' commits
        elif gg_arguments.commits is not None:
            current_invoke_return_values =\
                gatorgrader_invoke.invoke_commits_check(REPOSITORY,
                                                        gg_arguments.commits)
            check_return_values.append(current_invoke_return_values)
        # The requested check is not available
        else:
            print("Requested non-existent checking.")

        # DONE: Determine the correct exit code for the checks
        correct_exit_code = gatorgrader_exit.get_code(check_return_values)
        sys.exit(correct_exit_code)
