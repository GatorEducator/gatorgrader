"""GatorGrader checks the files of programmers and technical writers."""

import sys

from gator import orchestrate
from gator import checkers


if __name__ == "__main__":
    # assume that the checks pass and prove otherwise
    exit_code = 0
    # orchestrate check(s) of the specified deliverable(s)
    exit_code = orchestrate.check(sys.argv[1:])
    # exit the program with the correct code
    # error code: one aspect of the checks failed
    # normal code: all aspects of the checks passed
    sys.exit(exit_code)
