"""
MagicLexigen: Magic number language lexicon generator.

This script uses a modified nhentai.py api library to search through all English Doujinshis on NHentai.net
and rate them on the words they mention with a rating function.
If they perform best for a word, they are added as possible vocabulary for that word.
"""

import argparse
import csv
import re
import time
from functools import partial
from itertools import *
from math import inf
from random import random

from nhentai import Doujinshi

word = re.compile(r'\b([a-zA-Z]+)\b')

# an absolutely highest number of any doujinshi that may exist in the forseeable future
MAX_DOUJINSHI_COUNT = 400_000


def main():
    parser = argparse.ArgumentParser(description='NHentai magic number language lexicon generator.',
                                     epilog='NHentai content is not appropriate for minors and may be subject to copyright. The author takes no responsiblity nor provides liability for any content found on nhentai.net or indirectly through this script.')
    parser.add_argument('-n', '--count', dest='doujin_count', metavar='AMOUNT', action='store',
                        type=int, default=inf, help='The amount of doujinshis to process.')
    parser.add_argument('-s', '--spread', dest='doujin_skip', metavar='DISTRIBUTION', action='store', type=int, default=1,
                        help='The distribution of doujinshis that are considered. This option causes the process to only evaluate every DISTRIBUTION English Doujinshi.')
    parser.add_argument('-o', '--output', dest='outfile', action='store', type=(lambda fname: open(fname, 'w', newline='')), default='mnl_dictionary.csv',
                        help='The output CSV file where an English-to-MNL dictionary is written.')
    args = parser.parse_args()
    print(args)

    candidates = generateCandidates(args)
    # [print(c) for c in candidates]
    dictionary = generateDictionary(candidates, args)
    # print(dictionary)

    # write daa to csv
    writer = csv.writer(args.outfile)
    writer.writerow(("English word", "Magic number", "Ranking/Fitness"))
    # print(list(flatmap(lambda x: x, dictionary.items())))
    writer.writerows(
        map(lambda x: (x[0], x[1][0], x[1][1]), dictionary.items()))
    args.outfile.close()


def generateCandidates(args):
    """
    Generate the lexicon candidates from the NHentai Doujinshis as a giant list of (number, word, ranking) tuples
    """
    return (
        # 4. rate doujinshi's qualification for that word
        starmap(lambda douj, word: (douj.magic, word, default_rate(word, douj)),
                # 3. map doujinshis to a list of words to consider
                flatmap(lambda douj: zip(repeat(douj),
                                         # 3.5: the words to consider are all words in the title, all tags, and no duplicates
                                         set(chain(word.findall(douj.name), douj.tags))),
                        # 2. filter out invalid or unusable doujinshis
                        filter(lambda douj: douj is not None,
                               # 1. an iteration of a doujinshi request for every concievable doujinshi
                               map(make_doujinshi,
                                   # 0. generate a list of all possible magic numbers
                                   islice(count(1, args.doujin_skip), args.doujin_count)))))
    )


def make_doujinshi(magic):
    """Makes and returns a Doujinshi object from the given magic number."""
    try:
        # print("considering", magic)
        return Doujinshi(magic)
    except BaseException as e:
        return None


def flatmap(f, items: iter):
    '''Implements the common FP operation flatmap that maps elements and compresses them from a two-dimensional iterable to a one-dimensional iterable.'''
    return chain.from_iterable(map(f, items))


def generateDictionary(candidates: iter, args) -> dict:
    """Chooses the best-fitting number for each word and returns a dictionary with (number, ranking) tuples"""
    dictionary = {}
    count = 0
    start = lastUpdate = time.time()
    lastCount = 0
    for magic, word, ranking in candidates:
        if word in dictionary and dictionary[word][1] == ranking and random() > 0.5:
            # print("By randomness: in word {:20} replacing {!s} with {!s}.".format(
            #     word, dictionary[word], (magic, ranking)))
            dictionary[word] = (magic, ranking)
        # if word in dictionary and dictionary[word][1] < ranking:
            # print("for word", word, ": replacing",
            #       dictionary[word], "with", str((magic, ranking)))
        if word not in dictionary or dictionary[word][1] < ranking:
            dictionary[word] = (magic, ranking)
        count = count + 1
        if (ct := time.time()) - lastUpdate > 1:
            # estimate remaining time based on operations since last print, estimated total operations and time passed since last print
            estimateRemaining = (ct - lastUpdate) / ((count - lastCount) /
                                                     (args.doujin_count*20)) - (ct - start)
            print('{:4.2f}% done, {:02d}m{:02d}s remaining, at {:06d}'.format(
                (count / (args.doujin_count*20))*100, int(estimateRemaining/60), int(estimateRemaining % 60), magic))
            lastUpdate, lastCount = ct, count
    return dictionary


def default_rate(cur_word: str, douj: dict) -> int:
    """
    Default rating function. Rates a doujinshi's qualification to represent a given word
    according to the doujinshi's `tags` and `name`.

    All occurrances of the word in tags and name are added, while an occurance in the name counts four times as much.

    """
    # tags: List[str], name: str
    word_count = len(
        list(filter(lambda nword: nword == cur_word, word.findall(douj.name))))
    tag_count = 1 if cur_word in douj.tags else 0
    return word_count * 4 + tag_count


if __name__ == "__main__":
    main()
