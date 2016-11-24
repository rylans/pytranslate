'''Translator class'''

from english_model import EnglishModel
from translation_model import TranslationModel

class Translator(object):
    '''Combine translation model p(e1|f1) and language model p(e1|e0)'''
    def __init__(self, translation_model, production_model):
        self.translation_model = translation_model
        self.production_model = production_model
        self.filter_max = 16
        self.null_prior = 0.000007 #FIXME: problem with words being elided too much
        self.phi2_prior = 1.0

        #FIXME: Refactor this constructor
        if type(translation_model) == type(str()) and type(production_model) == type(str()):
            self.production_model = EnglishModel(production_model)
            tm = TranslationModel()
            tm.learn_from_text(translation_model, production_model)
            self.translation_model = tm

    def _combine_p_trans(self, p_trans1, p_trans2):
        '''Combine the words and probabilities inside both possible translations'''
        return (p_trans1[0] * p_trans2[0], p_trans1[1] + ' ' + p_trans2[1])

    def _fertility_2_combinations(self, possible_translations):
        '''Return combinations of two words

        Args:
            possible_translations (list): [(prob1, trans1) ... ]

        Returns:
            list: [(w1, w2), (w2, w1), (w3, w1) ... ]
        '''
        if possible_translations == None:
            return []
        if len(possible_translations) < 2:
            return []
        p_trans = possible_translations[:4]

        combos = []
        combos.append((p_trans[0], p_trans[1]))
        combos.append((p_trans[1], p_trans[0]))

        if len(p_trans) < 3:
            return combos

        # TODO: Do this algorithmically instead of manually
        combos.append((p_trans[0], p_trans[2]))
        combos.append((p_trans[1], p_trans[2]))
        combos.append((p_trans[2], p_trans[0]))
        combos.append((p_trans[2], p_trans[1]))

        if len(p_trans) < 4:
            return combos

        combos.append((p_trans[0], p_trans[3]))
        combos.append((p_trans[1], p_trans[3]))
        combos.append((p_trans[2], p_trans[3]))
        combos.append((p_trans[3], p_trans[0]))
        combos.append((p_trans[3], p_trans[1]))
        combos.append((p_trans[3], p_trans[2]))

        return combos

    def _next_word(self, source_word, prev_word=''):
        '''Translate source word into zero to two words and report probability

        p(e3 | f3) = p2 * p(f3 | e3) * p(e3 | e2)

        Args:
            source_word (string): the word in the source language to be translated
            prev_word (string): the translation of the previous word

        Returns:
            list: [ (probability_1, translated_word_1), (probability_2, translated_word_2) ... ]
        '''
        if prev_word == None:
            prev_word = ''
        list_of_p_trans = self.translation_model.translate_word(source_word, 6, True)
        phi = self.translation_model.fertility(source_word)

        if list_of_p_trans == None:
            return [(0.00001, '[no_translation_' + source_word + ']')]

        lst = []
        # append fertility=1 candidates
        for p_trans in list_of_p_trans:
            candidate_probability = p_trans[0] * self.production_model.probability(p_trans[1], prev_word) * phi[1]
            lst_item = (candidate_probability, p_trans[1])
            lst.append(lst_item)

        # append NULL-word candidate
        lst.append((self.null_prior * phi[0], None))

        # append fertility=2 candidates
        for phi2_combos in  self._fertility_2_combinations(list_of_p_trans):
            p_trans1, p_trans2 = phi2_combos[0], phi2_combos[1]
            joint_p, joint_trans = self._combine_p_trans(p_trans1, p_trans2)

            candidate_probability = self.phi2_prior * phi[2] * joint_p * \
                    self.production_model.probability(p_trans1[1], prev_word) * \
                    self.production_model.probability(p_trans2[1], p_trans1[1])

            lst.append((candidate_probability, joint_trans))

        return sorted(lst)[::-1]

    def _combine_next_word(self, candidates, source_word):
        '''Translate source word and make new candidate translations

        Args:
            candidates (list): [ (probability_1, translation_1), (probability_2, translation_2) ... ]
            source_word (string): Word in the source text to be transalted

        Returns:
            list: [ (updated_probability, updated_translation) ... ]
        '''
        updated_translations = []
        for candidate in candidates:
            for next_candidate in self._next_word(source_word, candidate[1]):
                combined_p = candidate[0] * next_candidate[0]
                part1 = candidate[1] or ''
                part2 = next_candidate[1] or ''

                combined_trans = part1
                if combined_trans == '':
                    combined_trans = part2
                else:
                    combined_trans += ' ' + part2
                combined_trans = combined_trans.strip()

                updated_translations.append((combined_p, combined_trans))
        return sorted(updated_translations)[::-1][:self.filter_max]

    def translate(self, raw_source_text):
        '''Translate source text word-by-word into target language'''
        raw_source_text = raw_source_text.strip()
        if raw_source_text == '':
            return ''
        iteration = 0
        candidates = []
        for source_word in self.translation_model.preprocess(raw_source_text):
            if iteration == 0:
                candidates = self._next_word(source_word)
            else:
                candidates = self._combine_next_word(candidates, source_word)
            iteration += 1
        return sorted(candidates)[::-1][0][1]

if __name__ == '__main__':
    fr = 'elle va manger avec moi.\nelle aime toi.\ntu et moi ensemble\njamais.\nje veux manger vite.\nelle va\navec.'
    en = 'she is going to eat with me.\nshe likes you.\nyou and me together\nnever.\ni want to eat quick.\nshe is going to\nwith.'
    trx = Translator(fr, en)
    assert trx.translate('elle va manger avec toi') == 'she is going eat with you'
