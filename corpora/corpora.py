import json


def get_hits(word, corpora):
    with open('data/russian.json', 'r') as f:
        russian = json.load(f)

    if word in russian:
        return russian[word][0]['<ruscorpora>hits_words']
    else:
        print(f"no {word} in dictionary, query to ruscorpora")
        word_chars = corpora.get_corpora_chars(word)
        return word_chars['hits_words']


def get_ipm(word, corpora):
    with open('data/russian.json', 'r') as f:
        russian = json.load(f)

    if word in russian:
        return russian[word][0]['<ruscorpora>word_ipm']
    else:
        print(f"no {word} in dictionary, query to ruscorpora")
        word_chars = corpora.get_corpora_chars(word)
        return word_chars['hits_words'] / word_chars['total_words'] * (10**6)
