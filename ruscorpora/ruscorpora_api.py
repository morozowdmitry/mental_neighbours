import urllib.request
from urllib.parse import quote, urlparse, parse_qs
from bs4 import BeautifulSoup

import time


class RusCorpora(object):
    """API class for RusCorpora (ruscorpora.ru)"""
    def __init__(self):
        self.sleeptime = 10

    def get_corpora_chars(self, word, ambiguity=False):
        url = self._create_url(quote(word), ambiguity)
        while True:
            result, soup = RusCorpora()._get_soup(url)
            if result:
                return RusCorpora()._extract_frequency(soup)
            elif not result and soup != 429:
                return RusCorpora()._extract_frequency()

    @staticmethod
    def _create_url(word, ambiguity=False):
        if ambiguity:
            return f'http://processing.ruscorpora.ru/search.xml?'\
                   f'mycorp=JSONeyJkb2NfaV90YWdnaW5nIjogWyIxIl19&'\
                   f'mysize=6003397&'\
                   f'mydocsize=2170&'\
                   f'text=lexgramm&'\
                   f'mode=main&'\
                   f'lex1={word}'
        else:
            return f'http://processing.ruscorpora.ru/search.xml?' \
                   f'text=lexgramm&' \
                   f'mode=main&' \
                   f'lex1={word}'

    def _get_soup(self, url):
        try:
            soup_url = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(self.sleeptime)
                self.sleeptime += 10
            return False, e.code
        try:
            soup = BeautifulSoup(soup_url, 'lxml')
            return True, soup
        except UnboundLocalError:
            print(parse_qs(urlparse(url).query))

    @staticmethod
    def _extract_frequency(soup=None):
        if not soup:
            return {"total_words": 0,
                    "total_docs": 0,
                    "hits_words": 0,
                    "hits_docs": 0}
        all_stats = [x.get_text() for x in soup.find_all(class_="stat-number")]
        if len(all_stats) == 0:
            return {"total_words": 0,
                    "total_docs": 0,
                    "hits_words": 0,
                    "hits_docs": 0}
        total_docs, total_words, word_docs, word_uses = [int(x.replace(' ', '')) for x in all_stats[2:]]
        frequency_chars = dict()
        frequency_chars['total_words'] = total_words
        frequency_chars['total_docs'] = total_docs
        frequency_chars['hits_words'] = word_uses
        frequency_chars['hits_docs'] = word_docs
        return frequency_chars
