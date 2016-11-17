'''Translator class'''

class Translator(object):
    def __init__(self, translation_model, production_model):
        self.translation_model = translation_model
        self.production_model = production_model
        self.filter_max = 8

    def _next_word(self, source_word, prev_word=''):
        '''Translate word and report probability

        p(e3 | f3) = p2 * p(f3 | e3) * p(e3 | e2)

        Args:
            source_word (string): the word in the source language to be translated
            prev_word (string): the translation of the previous word

        Returns:
            list: [ (probability_1, translated_word_1), (probability_2, translated_word_2) ... ]
        '''
        list_of_p_trans = self.translation_model.translate_word(source_word, 3, True)
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
        return ''

if __name__ == '__main__':
    from EnglishModel import EnglishModel
    from FrEnTranslator import FrEnTranslator

    en_model = EnglishModel(['austen-emma.txt'])
    trans_model = FrEnTranslator()
    fr_side = '''je suis une fille
je suis une banane rouge
je t'aime
elle est une fille
la banane.
une fille est allee.'''

    en_side = '''I am a girl
I am a red banana
I love you
she is a girl
the banana.
a girl has gone.'''

    trans_model.learn_from_text(fr_side, en_side)
    translator = Translator(trans_model, en_model)

    '''
    print translator._next_word('suis', 'i')
    print translator._next_word('une', 'am')
    print translator._next_word('fille', 'a')
    print translator._next_word('banane', 'the')
    print translator._next_word('banane', 'she')
    print translator._next_word('banane', 'a')
    print translator._next_word('rouge', 'a')
    '''

    tsp = translator._next_word('une' , 'am')
    print tsp
    tsp2 = translator._combine_next_word(tsp, 'fille')
    print tsp2
    tsp3 = translator._combine_next_word(tsp2, 'est')
    print tsp3
    tsp4 = translator._combine_next_word(tsp3, 'allee')
    print tsp4
    tsp5 = translator._combine_next_word(tsp4, '.')
    print tsp5
    print tsp5[0][1]


    fr_side = 'je vais aller ici'
    en_side = 'I want to go here'
    trans_model.learn_from_text(fr_side, en_side)
    translator = Translator(trans_model, en_model)
