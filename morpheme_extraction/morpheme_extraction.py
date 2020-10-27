import json

import pathlib
data_folder = pathlib.Path(__file__).parent.parent.absolute() / 'data/tikhonov_corrected'

from morpheme_extraction.NeuralMorphemeSegmentation.neural_morph_segm import Partitioner, measure_quality
from morpheme_extraction.NeuralMorphemeSegmentation.read import read_BMES


def predict_types(model, words):
    """Predict morphemes along with morpheme types.

    return list of two-element lists: for each word list of morphemes and list of types
        [
            [[morpheme11, ..., morpheme1N], [type11, ..., type1N]],
            ...
            [[morphemeK1, ..., morphemeKM], [typeK1, ..., typeKM]],
        ]
    """
    labels_with_probs = model._predict_probs(words)
    return [
        model.labels_to_morphemes(word, elem[0], elem[1], return_types=True)
        for elem, word in zip(labels_with_probs, words)
    ]


class MorphemePredictor(object):
    def __init__(self, nepochs):
        x_train, y_train = read_BMES(data_folder / 'tikhonov_train.txt')
        x_test, y_test = read_BMES(data_folder / 'tikhonov_test.txt')
        cls = Partitioner(nepochs=nepochs)
        cls.train(x_train, y_train, x_test, y_test, )
        self.model = cls

    def predict(self, lemma):
        prediction = predict_types(self.model, [lemma])[0]
        resulting_string = '/'.join([f"{x}:{y}" for x, y in zip(prediction[0], prediction[1])])
        return resulting_string


def extract_morphemes(lemma, predictor):
    with open(data_folder / 'tikhonov.json', 'r') as f:
        tikhonov_dict = json.load(f)
    if lemma in tikhonov_dict:
        return tikhonov_dict[lemma]
    else:
        return predictor.predict(lemma)
