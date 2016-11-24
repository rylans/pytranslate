'''evaluation methods for translator

Evaluate FR->EN on europarl
Evaluate more languages...
'''

from translator import Translator
from translation_model import TranslationModel
from english_model import EnglishModel
import time
import sys, os
sys.path.append(os.path.realpath('..'))

class TranslationScore(object):
    '''Score a translation'''
    def __init__(self):
        pass

    def of(self, actual_text, expected_text):
        tm = TranslationModel()
        actual_parts = tm.preprocess(actual_text)
        expected_parts = tm.preprocess(expected_text)

        if len(expected_parts) == 0:
            return 1.0

        actual_in_expected = 0
        for actual in actual_parts:
            if actual in expected_parts:
                actual_in_expected += 1
        true_positive = actual_in_expected/float(len(actual_parts))

        expected_not_in_actual = 0
        for expected in expected_parts:
            if expected not in actual_parts:
                expected_not_in_actual += 1
        maxlen = max(len(expected_parts), len(actual_parts))
        true_negative = 1.0 - expected_not_in_actual/float(maxlen)

        return true_positive * true_negative

def tdiff(past_t, now_t):
    delta = now_t - past_t
    return "{:0.1f}".format(delta)

def get_europarl_en_lines():
    with open('texts/europarl-sample.fr-en.en', 'r') as fl:
        return fl.readlines()

def get_europarl_fr_lines():
    with open('texts/europarl-sample.fr-en.fr', 'r') as fl:
        return fl.readlines()

def score_fr_en_europarl():
    print "\nFR->EN Europarl:"
    # max lines is 300 at the moment
    num_lines = 300
    num_chars = 50

    tstart = time.time()
    en_lines = get_europarl_en_lines()
    fr_lines = get_europarl_fr_lines()

    en_learn_set = []
    fr_learn_set = []
    en_eval_set = []
    fr_eval_set = []

    for index, pair in enumerate(zip(en_lines, fr_lines)[:num_lines]):
        pair0 = pair[0][:num_chars]
        pair1 = pair[1][:num_chars]
        if index%4 == 0:
            en_eval_set.append(pair0)
            fr_eval_set.append(pair1)
        else:
            en_learn_set.append(pair0)
            fr_learn_set.append(pair1)

    fr_text = '\n'.join(fr_learn_set)
    en_text = '\n'.join(en_learn_set)

    trx_model = TranslationModel()
    english = EnglishModel(['austen-emma.txt'])
    trx_model.learn_from_text(fr_text, en_text)
    translator = Translator(trx_model, english)

    scorer = TranslationScore()
    n = 0
    score = 0
    for xfr, xen in zip(fr_eval_set, en_eval_set):
        trx_en = translator.translate(xfr)
        n += 1
        score += scorer.of(trx_en, xen)
    avg_score = float(score)/n
    print "lines: ", num_lines, ", chars: ", num_chars
    print "Translation score: {:0.2f}".format(avg_score) + " (of " + str(n) + " comparisons)"
    tend = time.time()
    print tdiff(tstart, tend) + " seconds elapsed."

if __name__ == '__main__':
    score_fr_en_europarl()
