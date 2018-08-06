"""Handle the arguments provided to GatorGrader"""

import argparse


def parse(args):
    """Parses the arguments provided on the command-line"""
    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    gg_parser.add_argument(
        "--nowelcome", help="Do not display the welcome message", action="store_true"
    )

    gg_parser.add_argument("--checkfiles", nargs="+", type=str)
    gg_parser.add_argument("--directories", nargs="+", type=str)

    gg_parser.add_argument("--singlecomments", nargs="+", type=int)

    gg_parser.add_argument("--multicomments", nargs="+", type=int)

    gg_parser.add_argument("--paragraphs", nargs="+", type=int)
    gg_parser.add_argument(
        "--wordcount", "--sentences", nargs="+", type=int, dest="wordcount"
    )

    gg_parser.add_argument("--fragments", nargs="+", type=str)
    gg_parser.add_argument("--fragmentcounts", nargs="+", type=int)

    gg_parser.add_argument("--languages", nargs="+", type=str)

    gg_parser.add_argument("--commands", nargs="+", type=str)
    gg_parser.add_argument("--outputlines", nargs="+", type=int)

    gg_parser.add_argument("--commits", type=int)

    gg_arguments_finished = gg_parser.parse_args(args)
    return gg_arguments_finished


def verify(args):
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
    elif args.wordcount is not None:
        if args.checkfiles is None or args.directories is None:
            verified_arguments = False
    elif args.fragments is None and args.fragmentcounts is not None:
        verified_arguments = False
    return verified_arguments
