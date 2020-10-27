from pylev import levenshtein


def levenstein_close(word_first, word_second, max_dist=2):
    if word_first == word_second:
        return -1
    dist = levenshtein(word_first, word_second)
    if dist > min(max_dist, len(word_first) // 6 + 1, len(word_second) // 5 + 1):
        return -1
    return dist


def levenstein_neighborhood(word, dictionary):
    neighborhood = dict()
    for candidate in dictionary.keys():
        dist = levenstein_close(word, candidate, max_dist=2)
        if dist >= 0:
            neighborhood[candidate] = dist
    return neighborhood
