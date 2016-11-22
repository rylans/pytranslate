# -*- coding: UTF-8 -*-
import unittest

from pytranslate.Translator import Translator
from pytranslate.EnglishModel import EnglishModel
from pytranslate.FrEnTranslator import FrEnTranslator

class TestTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.english_model = EnglishModel(['austen-emma.txt', 'melville-moby_dick.txt'])

    def test_word_disambiguation_sa_fille(self):
        fr_text = 'Avec sa fille'
        en_text = 'With his daughter'

        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'avec sa fille', 'with his daughter')

    def test_word_disambiguation_mais_elle(self):
        fr_text = 'mais elle'
        en_text = 'she but'

        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'mais elle', 'but she')

    def test_new_translations_est_noir(self):
        fr_text = '''le chien est noir
le chat est noir
la vache est blanc
le texte
la pizza'''
        en_text = '''the dog is black
the cat is black
the cow is white
the text
the pizza'''
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'le chien est blanc', 'the dog is white')
        self._verify(trx, 'le chat est blanc', 'the cat is white')
        self._verify(trx, 'la vache est noir', 'the cow is black')
        self._verify(trx, 'la vache est le chat', 'the cow is the cat')

    def test_new_translations_qui_est(self):
        fr_text = '''qui est ici
elle est ici
il est rouge
il mange bien'''
        en_text = '''who is here
she is here
he is red
he eats well'''
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'qui est rouge', 'who is red')
        self._verify(trx, 'elle est rouge', 'she is red')
        self._verify(trx, 'qui mange ici', 'who eats here')
        self._verify(trx, 'il mange ici', 'he eats here')
        self._verify(trx, 'qui mange bien', 'who eats well')
        self._verify(trx, 'elle mange bien', 'she eats well')

    def test_word_not_in_text(self):
        fr_text = 'elle est'
        en_text = 'she is'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'Il', '[no-translation]')
        self._verify(trx, 'il est', '[no-translation] is')

    def test_blank_translation(self):
        fr_text = 'cette dame'
        en_text = 'this woman'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, '', '')

    def test_space_translation(self):
        fr_text = 'cette dame'
        en_text = 'this woman'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, ' ', '')

    def test_leading_space_translation(self):
        fr_text = 'mon ami'
        en_text = 'my friend'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, ' mon ami', 'my friend')

    def test_trailing_space_translation(self):
        fr_text = 'mon ami'
        en_text = 'my friend'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'mon ami ', 'my friend')

    def _verify(self, translator, source_text, expected_translation):
        self.assertTrue(translator.translate(source_text) == expected_translation)

    def _new_translator(self, fr_text, en_text, english_model):
        translation_model = FrEnTranslator()
        translation_model.learn_from_text(fr_text, en_text)
        return Translator(translation_model, english_model)

if __name__ == '__main__':
    unittest.main()
