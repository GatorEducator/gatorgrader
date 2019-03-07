"""Handle the arguments provided to GatorGrader"""

import argparse

JAVA = "Java"
PYTHON = "Python"


def parse(args):
    """Parses the arguments provided on the command-line"""
    # create the parser with the default help formatter
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # do not display the welcome message
    # CORRECT WHEN: always, only changes output on screen
    gg_parser.add_argument(
        "--nowelcome", help="do not display the welcome message", action="store_true"
    )

    # output reports in JSON
    # CORRECT WHEN: always, only changes report output
    gg_parser.add_argument("--json", help="print reports in JSON", action="store_true")

    # Top-Level Arguments {{{

    # specify a check for the number of commits in the Git repository
    # CORRECT WHEN: user provides this argument but not any other main arguments
    gg_parser.add_argument("--commits", type=int, help="minimum number of git commits")

    # specify a single file and a single directory
    # CORRECT WHEN: user provides both of these
    gg_parser.add_argument(
        "--directory", type=str, metavar="DIR", help="directory with file for checking"
    )
    gg_parser.add_argument("--file", type=str, help="file for checking")

    # Ancillary Arguments for File and Directory {{{

    # do not display the welcome message
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--exists", help="does a file in a directory exist", action="store_true"
    )

    # specify a check on single-line comments
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--single", type=int, metavar="COUNT", help="minimum number of single comments"
    )

    # specify a check on multiple-line comments
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--multiple", type=int, metavar="COUNT", help="minimum number of multi comments"
    )

    # specify that the comment checks are for a certain language
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--language",
        type=str,
        choices=[JAVA, PYTHON],
        help="language for the single comments",
    )

    # specify a check on paragraphs
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--paragraphs", metavar="COUNT", type=int, help="minimum number of paragraphs"
    )

    # specify a check on words
    # note that sentences are no longer supported so, a "dest" given
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--words", type=int, help="minimum number of words in paragraphs"
    )

    # }}}

    # specify a command to run for checking
    # CORRECT WHEN: user provides this argument but not a file or directory
    gg_parser.add_argument("--command", type=str, help="command to run")

    # execute the specified command
    # CORRECT WHEN: user provides a command to run along with this argument
    gg_parser.add_argument(
        "--executes", help="does a command execute without error", action="store_true"
    )

    # Ancillary Arguments for File or Commands {{{

    # specify a check on fragments
    # CORRECT WHEN: user provides file and directory along with this argument
    # or
    # CORRECT WHEN: user provides a command along with this argument
    gg_parser.add_argument(
        "--fragment", type=str, help="fragment that exists in code or output"
    )

    # specify a check on check_regex_file
    # CORRECT WHEN: user provides file and directory along with this arguments
    # or
    # CORRECT WHEN: user provides a command along with this argument
    gg_parser.add_argument(
        "--regex", type=str, help="regular expression that exists in code or output"
    )

    # specify a check on fragments
    # CORRECT WHEN: user provides file and directory along with this argument
    # or
    # CORRECT WHEN: user provides a command along with this argument
    gg_parser.add_argument(
        "--count", type=int, metavar="COUNT", help="how many of an entity should exist"
    )

    # }}}

    # Ancillary Arguments for Any Counting of Entities {{{

    # perform exact checking for entity counting (i.e,. "==" instead of ">=")
    # CORRECT WHEN: user provides file and directory along with this argument
    gg_parser.add_argument(
        "--exact", help="equals instead of a minimum number", action="store_true"
    )

    # }}}

    # call argparse's parse_args function and return result
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
    """Checks if it is a valid command specification"""
    if args.command is not None:
        return True
    return False


def is_valid_commits(args):
    """Checks if it is a valid commits specification"""
    if args.commits is not None:
        return True
    return False


# }}}

# Ancillary helper functions {{{


def is_valid_exact(args, skip=False):
    """Checks if it is a valid exact count specification"""
    # pylint: disable=bad-continuation
    if (
        is_valid_commits(args)
        or is_valid_comments(args)
        or is_valid_paragraphs(args)
        or is_valid_words(args)
        or is_valid_count(args)
        or is_valid_fragment(args)
        or is_valid_regex(args)
        or skip
    ):
        if args.exact is not False:
            return True
    return False


def is_valid_exists(args, skip=False):
    """Checks if it is a valid existence specification"""
    if is_valid_file_and_directory(args) or skip:
        if args.exists is not False:
            return True
    return False


def is_valid_comments(args, skip=False):
    """Checks if it is a valid comments specification"""
    if is_valid_file_and_directory(args) or skip:
        if args.single is not None or args.multiple is not None:
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


def is_valid_language(args, skip=False):
    """Checks if it is a valid language specification"""
    if (is_valid_file_and_directory(args) and is_valid_comments(args)) or skip:
        if args.language is not None:
            return True
    return False


def is_valid_executes(args, skip=False):
    """Checks if it is a valid executes without error specification"""
    if is_valid_command(args) or skip:
        if args.executes is not False:
            return True
    return False


def is_valid_fragment(args, skip=False):
    """Checks if it is a valid fragment specification"""
    if (is_valid_file_and_directory(args) or is_valid_command(args)) or skip:
        if args.fragment is not None and args.count is not None:
            return True
    return False


def is_valid_regex(args, skip=False):
    """Checks if it is a valid regex specification"""
    if (is_valid_file_and_directory(args) or is_valid_command(args)) or skip:
        if args.regex is not None and args.count is not None:
            return True
    return False


def is_valid_count(args, skip=False):
    """Checks if it is a valid count specification"""
    if (is_valid_file_and_directory(args) or is_valid_command(args)) or skip:
        if args.count is not None and args.fragment is None and args.regex is None:
            return True
    return False


def is_file_ancillary(args):
    """Checks if it is an ancillary of a file"""
    # pylint: disable=bad-continuation
    if (
        # skip the parent check and only
        # determine if the parameter is present
        is_valid_exists(args, skip=True)
        or is_valid_comments(args, skip=True)
        or is_valid_paragraphs(args, skip=True)
        or is_valid_words(args, skip=True)
    ):
        return True
    return False


def is_command_ancillary(args):
    """Checks if it is an ancillary of a command"""
    # pylint: disable=bad-continuation
    if (
        # skip the parent check and only
        # determine if the parameter is present
        is_valid_executes(args, skip=True)
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
    # TOP-LEVEL VERIFIED:
    # both a file and a directory were specified and a command is not given
    # pylint: disable=bad-continuation
    if is_valid_file_and_directory(args) and (
        not is_command_ancillary(args)
        and not is_valid_command(args)
        and not is_valid_commits(args)
    ):
        # track how many of the sub-arguments separately verified
        file_verified = []
        # VERIFIED: correct check for existence of a file in a directory
        if is_valid_exists(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for comments with language in a file in a directory
        if is_valid_comments(args) and is_valid_language(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for paragraphs in a file in a directory
        if is_valid_paragraphs(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for words in a file in a directory
        if is_valid_words(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for fragments in a file in a directory
        if is_valid_fragment(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for regex in a file in a directory
        if is_valid_regex(args):
            # verified arguments = True
            file_verified.append(True)
        # VERIFIED: correct check for line count of a file in a directory
        if is_valid_count(args):
            # verified_arguments = True
            file_verified.append(True)
        # VERIFIED: only one of prior valid options specified
        if file_verified.count(True) == 1:
            verified_arguments = True
    # TOP-LEVEL VERIFIED:
    # no file or directory details were specified and a command given
    # pylint: disable=bad-continuation
    elif is_valid_command(args) and (
        not is_valid_file_or_directory(args)
        and not is_file_ancillary(args)
        and not is_valid_commits(args)
    ):
        # track how many of the sub-arguments separately verified
        command_verified = []
        # VERIFIED: correct check for existence of a file in a directory
        if is_valid_executes(args):
            command_verified.append(True)
            # verified_arguments = True
        # VERIFIED: correct check for fragments in a file in a directory
        if is_valid_fragment(args):
            # verified_arguments = True
            command_verified.append(True)
        # VERIFIED: correct check for regex in a file in a directory
        # if is_valid_regex(args):
            # verified_arguments = True
            # command_verified.append(True)
        # VERIFIED: correct check for line count of a file in a directory
        if is_valid_count(args):
            # verified_arguments = True
            command_verified.append(True)
        # VERIFIED: only one of prior valid options specified
        if command_verified.count(True) == 1:
            verified_arguments = True
    # TOP-LEVEL VERIFIED:
    # no file or directory details were specified or a command given
    # and the argument is a request to check the count of Git commits
    # pylint: disable=bad-continuation
    elif is_valid_commits(args) and (
        not is_valid_file_or_directory(args)
        and not is_file_ancillary(args)
        and not is_valid_command(args)
        and not is_command_ancillary(args)
    ):
        verified_arguments = True
    return verified_arguments


# }}}
