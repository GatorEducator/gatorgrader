"""GatorGrader checks the files of programmers and technical writers."""

import sys

import gator


def main():
    """Run GatorGrader."""
    # orchestrate check given by the command line arguments
    exit_code = gator.grader_cli(sys.argv[1:])
    # exit the program with the returned code
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
