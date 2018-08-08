"""Handle the arguments provided to GatorGrader"""

import argparse


def parse(args):
    """Parses the arguments provided on the command-line"""
    # create the parser with the default help formatter
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # do not display the welcome message
    # CORRECT WHEN: user does or does not provide
    gg_parser.add_argument(
        "--nowelcome", help="Do not display the welcome message", action="store_true"
    )

    # Top-Level Arguments {{{

    # specify a single file and a single directory
    # CORRECT WHEN: user provides both of these
    gg_parser.add_argument(
        "--directory", type=str, help="Specify the directory with files for checking"
    )
    gg_parser.add_argument("--file", type=str, help="Specify the file for checking")

    # specify a command to run for checking
    # CORRECT WHEN: user provides this argument but not a file or directory
    gg_parser.add_argument("--command", type=str, help="Specify a command to run")

    # }}}

    # Ancillary Arguments {{{

    # specify a check on single-line comments
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--singlecomments",
        type=int,
        help="Specify a minimum number of single-line comments",
    )

    # specify a check on multiple-line comments
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--multicomments",
        type=int,
        help="Specify a minimum number of multiple-line comments",
    )

    # specify a check on paragraphs
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--paragraphs", help="Specify a minimum number of paragraphs"
    )

    # specify a check on words
    # note that sentences are no longer supported so, a "dest" given
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--words", "--sentences", dest="words", help="Specify a minimum number of words"
    )

    # specify a check on fragments
    # CORRECT WHEN: user provides file and directory along with this argument
    # or
    # CORRECT WHEN: user provides a command along with this argument
    gg_parser.add_argument("--fragment", type=str)
    gg_parser.add_argument("--fragmentcount", type=int)

    # }}}

    gg_parser.add_argument("--languages", nargs="+", type=str)

    gg_parser.add_argument("--outputlines", nargs="+", type=int)

    gg_parser.add_argument("--commits", type=int)

    gg_arguments_finished = gg_parser.parse_args(args)
    return gg_arguments_finished


# Helper functions {{{

# Top-level helper functions {{{


def is_valid_file(args):
    """Checks if it is a valid file and directory specification"""
    if args.file is not None:
        return True
    return False


def is_valid_directory(args):
    """Checks if it is a valid directory specification"""
    if args.directory is not None:
        return True
    return False


def is_valid_file_and_directory(args):
    """Checks if it is a valid file and directory specification"""
    if is_valid_file(args) and is_valid_directory(args):
        return True
    return False


def is_valid_file_or_directory(args):
    """Checks if it is a valid file or directory specification"""
    if is_valid_file(args) or is_valid_directory(args):
        return True
    return False


def is_valid_command(args):
    """Checks if it is a valid commands specification"""
    if args.command is not None:
        return True
    return False


# }}}

# Ancillary helper functions {{{


def is_valid_comments(args, skip=False):
    """Checks if it is a valid comment specification"""
    if is_valid_file_and_directory(args) or skip:
        if args.singlecomments is not None or args.multicomments is not None:
            return True
    return False


def is_valid_paragraphs(args, skip=False):
    """Checks if it is a valid paragraphs specification"""
    if is_valid_file_and_directory(args) or skip:
        if args.paragraphs is not None:
            return True
    return False


def is_valid_words(args, skip=False):
    """Checks if it is a valid words specification"""
    if is_valid_file_and_directory(args) or skip:
        if args.words is not None:
            return True
    return False


def is_valid_fragment(args, skip=False):
    """Checks if it is a valid fragment specification"""
    if (is_valid_file_and_directory(args) or is_valid_command(args)) or skip:
        if args.fragment is not None and args.fragmentcount is not None:
            return True
    return False


def is_file_ancillary(args):
    """Checks if it is an ancillary of a file"""
    # pylint: disable=bad-continuation
    if (
        # skip the parent check and only
        # determine if the parameter is present
        is_valid_comments(args, skip=True)
        or is_valid_paragraphs(args, skip=True)
        or is_valid_words(args, skip=True)
    ):
        return True
    return False


# }}}

# }}}

# Verification function {{{


def verify(args):
    """Checks if the arguments are correct"""
    # assume that the arguments are not valid and prove otherwise
    verified_arguments = False
    # TOP-LEVEL VERIFIED: both a file and a directory were specified and a command is not given
    if is_valid_file_and_directory(args) and not is_valid_command(args):
        verified_arguments = True
        # VERIFIED: correct check for comments of a file in a directory
        if is_valid_comments(args):
            verified_arguments = True
        # VERIFIED: correct check for paragraphs of a file in a directory
        if is_valid_paragraphs(args):
            verified_arguments = True
        # VERIFIED: correct check for words of a file in a directory
        if is_valid_words(args):
            verified_arguments = True
    # TOP-LEVEL VERIFIED: no file or directory details were specified and a command given
    # pylint: disable=bad-continuation
    elif is_valid_command(args) and (
        not is_valid_file_or_directory(args) and not is_file_ancillary(args)
    ):
        verified_arguments = True
    return verified_arguments


# }}}
