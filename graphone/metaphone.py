import re


def _collapse_duplicates(word):
    result = re.sub(r"(.)\1+", r"\1", word)
    return result


def _iotated_conversion(word):
    tmp_result = re.sub(r"йо", r"ё", word)
    result = re.sub(r"йе|йэ|ие", r"е", tmp_result)
    return result


def _vowel_conversion(word):
    tmp_result = re.sub(r"[оыя]", r"а", word)
    tmp_result = re.sub(r"[еёэ]", r"и", tmp_result)
    result = re.sub(r"ю", r"у", tmp_result)
    return result


def _voicelessness_conversion(word):
    conversion_dict = {'б': 'п',
                       'д': 'т',
                       'в': 'ф',
                       'з': 'с',
                       'ж': 'ш',
                       'г': 'к'}
    blockers = 'аяуюэеоёыилмнр'
    result = ''
    for idx, symbol in enumerate(word):
        if idx + 1 == len(word) or word[idx + 1] not in blockers:
            result += conversion_dict.get(symbol, symbol)
        else:
            result += symbol
    return result


def _bigram2c_conversion(word):
    result = re.sub(r"дс|тс", r"ц", word)
    return result


def _signs_deletion(word):
    result = re.sub(r"[ьъ]", r"", word[:-1]) + word[-1]
    return result


def convert2metaphone_code(word):
    tmp_code = _collapse_duplicates(word)
    tmp_code = _iotated_conversion(tmp_code)
    tmp_code = _vowel_conversion(tmp_code)
    tmp_code = _voicelessness_conversion(tmp_code)
    tmp_code = _bigram2c_conversion(tmp_code)
    tmp_code = _collapse_duplicates(tmp_code)
    code = _signs_deletion(tmp_code)
    return code


def metaphone_neighborhood(word, dictionary, convert_dictionary=True):
    neighborhood = list()
    word_code = convert2metaphone_code(word)
    if convert_dictionary:
        for candidate in dictionary.keys():
            candidate_code = convert2metaphone_code(candidate)
            if candidate_code == word_code and candidate != word:
                neighborhood.append(candidate)
    else:
        for candidate, code in dictionary.items():
            if code == word_code and candidate != word:
                neighborhood.append(candidate)
    return neighborhood
