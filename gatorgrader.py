"""GatorGrader checks the files of programmers and technical writers."""

import sys

from gator import orchestrate


def main():
    """Run GatorGrader."""
    # orchestrate check(s) of the specified deliverable(s)
    exit_code = orchestrate.main_cli(sys.argv[1:])
    # exit the program with the correct code
    # error code: one aspect of the checks failed
    # normal code: all aspects of the checks passed
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
