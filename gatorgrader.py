""" GatorGrader checks the files of programmers and writers """

import argparse
import sys

import gatorgrader_files


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
    return verified_arguments


if __name__ == '__main__':
    # parse and verify the arguments
    gg_arguments = parse_gatorgrader_arguments(sys.argv[1:])
    did_verify_arguments = verify_gatorgrader_arguments(gg_arguments)
    if did_verify_arguments is False:
        sys.exit(1)
