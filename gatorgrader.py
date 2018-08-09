"""GatorGrader checks the files of programmers and writers"""

import sys

from gator import arguments
from gator import display
from gator import invoke
from gator import leave


DEFAULT_COUNT = 0
DEFAULT_LANGUAGE = "Java"
INCORRECT_ARGUMENTS = 2
NONEXISTENT_CHECKING = 3
JAVA = "Java"
PYTHON = "Python"

SINGLE = "single-line"
MULTIPLE = "multiple-line"

REPOSITORY = "."


if __name__ == "__main__":
    # parse and verify the arguments
    gg_arguments = arguments.parse(sys.argv[1:])
    did_verify_arguments = arguments.verify(gg_arguments)
    # incorrect arguments, exit program
    if did_verify_arguments is False:
        # still permitted to display messages
        if gg_arguments.nowelcome is not True:
            display.welcome_message()
        # display incorrect arguments message
        display.incorrect_message()
        # exit given that arguments are wrong
        sys.exit(INCORRECT_ARGUMENTS)
    # correct arguments, so perform the checks
    else:
        # still permitted to display messages
        if gg_arguments.nowelcome is not True:
            display.welcome_message()
            display.checking_message()
        check_return_values = []
        # CHECK: all of the files exist in their directory
        if gg_arguments.directory is not None and gg_arguments.file is not None:
            current_invoke_return_values = invoke.invoke_all_file_in_directory_checks(
                gg_arguments.file, gg_arguments.directory
            )
            check_return_values.extend(current_invoke_return_values)
            # CHECK: Java code contains 'k' single-line comments
            if gg_arguments.singlecomments is not None:
                current_invoke_return_values = invoke.invoke_all_comment_checks(
                    gg_arguments.file,
                    gg_arguments.directory,
                    gg_arguments.singlecomments,
                    SINGLE,
                    gg_arguments.language,
                )
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Java code contains 'k' multiple-line comments
            if gg_arguments.multicomments is not None:
                current_invoke_return_values = invoke.invoke_all_comment_checks(
                    gg_arguments.file,
                    gg_arguments.directory,
                    gg_arguments.multicomments,
                    MULTIPLE,
                    gg_arguments.language,
                )
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Writing contains 'k' paragraphs
            if gg_arguments.paragraphs is not None:
                current_invoke_return_values = invoke.invoke_all_paragraph_checks(
                    gg_arguments.file,
                    gg_arguments.directory,
                    gg_arguments.paragraphs,
                )
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Writing all paragraphs contain 'k' words
            if gg_arguments.words is not None:
                current_invoke_return_values = invoke.invoke_all_word_count_checks(
                    gg_arguments.file,
                    gg_arguments.directory,
                    gg_arguments.words,
                )
                check_return_values.extend(current_invoke_return_values)
            # CHECK: Content contains 'k' specified fragment
            # pylint: disable=bad-continuation
            if (
                gg_arguments.fragment is not None
                and gg_arguments.fragmentcount is not None
            ):
                current_invoke_return_values = invoke.invoke_all_fragment_checks(
                    gg_arguments.file,
                    gg_arguments.directory,
                    gg_arguments.fragment,
                    gg_arguments.fragmentcount,
                )
                check_return_values.extend(current_invoke_return_values)
        # CHECK: Command produces 'k' lines of output
        elif gg_arguments.commands is not None and gg_arguments.outputlines is not None:
            current_invoke_return_values = invoke.invoke_all_command_checks(
                gg_arguments.commands, gg_arguments.outputlines
            )
            check_return_values.extend(current_invoke_return_values)
        # CHECK: Command produces lines of output with the specified fragment
        elif gg_arguments.commands is not None and gg_arguments.fragment is not None:
            current_invoke_return_values = invoke.invoke_all_command_fragment_checks(
                gg_arguments.commands, gg_arguments.fragment
            )
            check_return_values.extend(current_invoke_return_values)
        # CHECK: Repository contains at least 'k' commits
        elif gg_arguments.commits is not None:
            current_invoke_return_values = invoke.invoke_commits_check(
                REPOSITORY, gg_arguments.commits
            )
            check_return_values.append(current_invoke_return_values)
        # The requested check is not available
        else:
            print("Requested non-existent checking.")
            sys.exit(NONEXISTENT_CHECKING)

        # DONE: Determine the correct exit code for the checks
        correct_exit_code = leave.get_code(check_return_values)
        sys.exit(correct_exit_code)
