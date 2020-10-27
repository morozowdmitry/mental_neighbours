from pylev import levenshtein

import json

import pathlib
data_folder = pathlib.Path(__file__).parent.parent.absolute() / 'data'


def levenstein_close(word_first, word_second, max_dist=2):
    if word_first == word_second:
        return -1
    dist = levenshtein(word_first, word_second)
    if dist > min(max_dist, len(word_first) // 6 + 1, len(word_second) // 5 + 1):
        return -1
    return dist


def levenstein_neighborhood(word, dictionary=None):
    neighborhood = dict()
    if not dictionary:
        with open(data_folder / 'tikhonov_corrected/tikhonov.json', 'r') as f:
            dictionary = json.load(f)
    for candidate in dictionary.keys():
        dist = levenstein_close(word, candidate, max_dist=2)
        if dist >= 0:
            neighborhood[candidate] = dist
    return list(neighborhood.keys())
