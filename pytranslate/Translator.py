'''Translator class'''

class Translator(object):
    '''Combine translation model p(e1|f1) and language model p(e1|e0)'''
    def __init__(self, translation_model, production_model):
        self.translation_model = translation_model
        self.production_model = production_model
        self.filter_max = 16

    def _next_word(self, source_word, prev_word=''):
        '''Translate word and report probability

        p(e3 | f3) = p2 * p(f3 | e3) * p(e3 | e2)

        Args:
            source_word (string): the word in the source language to be translated
            prev_word (string): the translation of the previous word

        Returns:
            list: [ (probability_1, translated_word_1), (probability_2, translated_word_2) ... ]
        '''
        list_of_p_trans = self.translation_model.translate_word(source_word, 6, True)
        if list_of_p_trans == None:
            return [(0.00001, '[no-translation]')]
        lst = [(p_trans[0]*self.production_model.probability(p_trans[1], prev_word), p_trans[1]) for p_trans in list_of_p_trans]
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
                combined_trans = candidate[1] + ' ' + next_candidate[1]
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
