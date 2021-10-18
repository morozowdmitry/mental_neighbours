import requests
import json


import time


class RusCorpora(object):
    """API class for RusCorpora (ruscorpora.ru)"""
    def __init__(self):
        self.sleeptime = 10
        self.ambiguity = False

    def get_corpora_chars(self, word, ambiguity=False):
        self.ambiguity = ambiguity
        url = self._create_url(quote(word), ambiguity)
        while True:
            response = self._get_json(url)
            if response.status_code == 200:
                return self._extract_frequency_json(response.text)

    @staticmethod
    def _create_url(word, ambiguity=False):
        if ambiguity:
            # FIXME temporary disabled
            # return f'https://processing.ruscorpora.ru/search.xml?'\
            #        f'mycorp=JSONeyJkb2NfaV90YWdnaW5nIjogWyIxIl19&'\
            #        f'mysize=6003397&'\
            #        f'mydocsize=2170&'\
            #        f'text=lexgramm&'\
            #        f'mode=main&'\
            #        f'lex1={word}'
            return ''
        else:
            return f'https://processing.ruscorpora.ru/search.xml?' \
                   f'text=lexgramm&' \
                   f'mode=main&' \
                   f'lex1={word}&' \
                   f'format=json'

    def _get_json(self, url):
        response = requests.get(url)
        if response.status_code == 429:
            time.sleep(self.sleeptime)
            self.sleeptime += 10
        return response

    def _extract_frequency_json(self, response):
        data = json.loads(response)
        frequency_chars = dict()
        frequency_chars['total_words'] = data['corp_stat']['stats'][1]['num']
        frequency_chars['total_docs'] = data['corp_stat']['stats'][0]['num']
        if data['found_stat']['stats']:
            frequency_chars['hits_words'] = data['found_stat']['stats'][1]['num']
            frequency_chars['hits_docs'] = data['found_stat']['stats'][0]['num']
        else:
            frequency_chars['hits_words'] = 0
            frequency_chars['hits_docs'] = 0
        return frequency_chars


if __name__ == "__main__":
    corpora = RusCorpora()
    print(corpora.get_corpora_chars('fsad'))
