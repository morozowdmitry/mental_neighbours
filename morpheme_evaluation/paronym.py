import json
from collections import Counter

import re

from ruscorpora.ruscorpora_api import RusCorpora

import pathlib
data_folder = pathlib.Path(__file__).parent.parent.absolute() / 'data'


def delete_endings(parsing):
    return [x for x in parsing if x[-3:] != 'END']


def construct_word_from_morphemes(parsing):
    result = ''
    for morpheme in parsing:
        result += morpheme.split(':')[0]
    return result


def guess_ending(endings, parsing):
    candidates = {parsing}
    for ending in endings:
        if ending + ':END' in parsing:
            for ending_candidate in endings:
                candidates.add(re.sub(ending, ending_candidate, parsing))
    return list(candidates)


def create_possible_paronyms(parsing):
    with open(data_folder / 'tikhonov_corrected/tikhonov.json', 'r') as f:
        tikhonov_dict = json.load(f)
    with open(data_folder / 'paronym_pairs.txt', 'r') as f:
        data = f.readlines()

    paronym_rules = dict()
    for row in data:
        first_sequence, second_sequence = row.strip().split('->')
        if first_sequence in paronym_rules:
            paronym_rules[first_sequence].append(second_sequence)
        else:
            paronym_rules[first_sequence] = [second_sequence]

    endings = ['ий', 'ой', 'ый']
    paronyms = []

    for rule in paronym_rules.keys():
        if rule == '':
            divided_parsing = parsing.split('/')
            was_root = False
            for idx, morpheme in enumerate(divided_parsing):
                for option in paronym_rules[rule]:
                    if not was_root and option.endswith('PREF'):
                        candidate = '/'.join(divided_parsing[:idx] + [option] + divided_parsing[idx:])
                        candidates = guess_ending(endings, candidate)
                        candidates = [construct_word_from_morphemes(x.split('/')) for x in candidates]
                        paronyms.append(candidates)
                    elif was_root and option.endswith('SUFF'):
                        candidate = '/'.join(divided_parsing[:idx] + [option] + divided_parsing[idx:])
                        candidates = guess_ending(endings, candidate)
                        candidates = [construct_word_from_morphemes(x.split('/')) for x in candidates]
                        paronyms.append(candidates)
                if morpheme[-4:] == 'ROOT':
                    was_root = True
        elif rule != '' and ('/' + rule + '/' in parsing or
                             parsing.startswith(rule + '/') or
                             parsing.endswith('/' + rule)):
            for option in paronym_rules[rule]:
                candidate = re.sub(rule, option, parsing)
                if ':END' in candidate:
                    candidates = guess_ending(endings, candidate)
                    candidates = [construct_word_from_morphemes(x.split('/')) for x in candidates]
                    paronyms.append(candidates)
                else:
                    word = construct_word_from_morphemes(candidate.split('/'))
                    paronyms.append([word])
    # print(paronyms)
    ruscorpora = RusCorpora()
    validated_paronyms = []
    for paronym_group in paronyms:
        in_tikhonov = False
        for paronym in paronym_group:
            if paronym in tikhonov_dict:
                validated_paronyms.append(paronym)
                in_tikhonov = True
                # print(paronym)
                break
        if not in_tikhonov:
            for paronym in paronym_group:
                if ruscorpora.get_corpora_chars(paronym)['hits_words'] > 5:
                    validated_paronyms.append(paronym)
                    # print(paronym)
                    break

    # paronyms = [x for x in paronyms if ruscorpora.word_chars(x)['<ruscorpora>hits_words'] > 0]
    return list(set(validated_paronyms))


