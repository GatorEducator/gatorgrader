""" Utility functions that check the comments of a file """

import re

# References:
# https://stackoverflow.com/questions/18568105/how-match-a-paragraph-using-regex
# https://stackoverflow.com/questions/13531204/how-to-match-paragraphs-in-text-with-regx

PARAGRAH_RE = r'(.+?\n\n|.+?$)'


def count_paragraphs(contents):
    """ Counts the number of paragraphs in the writing """
    pattern = re.compile(PARAGRAH_RE, re.DOTALL)
    matches = pattern.findall(contents)

    return len(matches)
