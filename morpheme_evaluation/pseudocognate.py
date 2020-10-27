import json

import re

import pathlib
data_folder = pathlib.Path(__file__).parent.parent.absolute() / 'data'


def cut_possible_postfixes(word, postfixes):
    pseudoroots = {word}

    for postfix in postfixes:
        if word.endswith(postfix):
            pseudoroots.add(word[:-len(postfix)])
    return pseudoroots


def cut_possible_endings(word, endings):
    pseudoroots = {word}

    for ending in endings:
        if word.endswith(ending):
            pseudoroots.add(word[:-len(ending)])
    return pseudoroots


def cut_possible_prefixes(word, prefixes):
    pseudoroots = {word}

    can_cut = True
    while can_cut:
        new_pseudoroots = set()
        for prefix in prefixes:
            for option in pseudoroots:
                pseudoroot = option.split('/')[-1]
                existing_prefixes = option.split('/')[:-1]
                if pseudoroot.startswith(prefix) and prefix not in existing_prefixes:
                    new_pseudoroots.add('/'.join(existing_prefixes + [prefix] + [pseudoroot[len(prefix):]]))
        if new_pseudoroots.issubset(pseudoroots):
            can_cut = False
        pseudoroots.update(new_pseudoroots)
    pseudoroots = {x.split('/')[-1] for x in pseudoroots}
    return pseudoroots


def cut_possible_suffixes(word, suffixes):
    pseudoroots = {word}

    can_cut = True
    while can_cut:
        new_pseudoroots = set()
        for suffix in suffixes:
            for option in pseudoroots:
                pseudoroot = option.split('/')[0]
                existing_suffixes = option.split('/')[1:]
                if pseudoroot.endswith(suffix) and suffix not in existing_suffixes:
                    new_pseudoroots.add('/'.join([pseudoroot[:-len(suffix)]] + [suffix] + existing_suffixes))
        if new_pseudoroots.issubset(pseudoroots):
            can_cut = False
        pseudoroots.update(new_pseudoroots)
    pseudoroots = {x.split('/')[0] for x in pseudoroots}
    return pseudoroots


def find_possible_pseudoroots(root):
    pseudoroots = {root}

    with open(data_folder / 'known_affixes/known_prefixes.txt', 'r') as f:
        prefixes = [x.strip() for x in f.readlines() if x.strip() != '']

    with open(data_folder / 'known_affixes/known_suffixes.txt', 'r') as f:
        suffixes = [x.strip() for x in f.readlines() if x.strip() != '']

    roots_with_cutted_prefixes = set()
    new_pseudoroots = cut_possible_prefixes(root, prefixes)
    roots_with_cutted_prefixes.update(new_pseudoroots)

    roots_with_cutted_suffixes = set()
    new_pseudoroots = cut_possible_suffixes(root, suffixes)
    roots_with_cutted_suffixes.update(new_pseudoroots)

    pseudoroots.update(roots_with_cutted_prefixes)
    pseudoroots.update(roots_with_cutted_suffixes)

    if '' in pseudoroots:
        pseudoroots.remove('')
    pseudoroots.remove(root)

    return [x for x in pseudoroots if len(x) > 1]


def find_pseudocognate(parsing):
    root = [x.split(':')[0] for x in parsing.split('/') if x.endswith('ROOT')][0]
    with open(data_folder / 'tikhonov_corrected/tikhonov.json', 'r') as f:
        tikhonov_dict = json.load(f)
    pseudoroots = find_possible_pseudoroots(root)
    if not pseudoroots:
        return list()
    neighborhood = set()
    for word, parsing in tikhonov_dict.items():
        for morpheme in parsing.split('/'):
            morpheme_value, morpheme_type = morpheme.split(':')
            if morpheme_type == 'ROOT' and morpheme_value in pseudoroots:
                neighborhood.add(word)
    return list(neighborhood)
