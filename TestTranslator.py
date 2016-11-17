import unittest

from Translator import Translator
from EnglishModel import EnglishModel
from FrEnTranslator import FrEnTranslator

class TestTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.english_model = EnglishModel(['austen-emma.txt'])

    def test_word_disambiguation_from_corpus_sa_fille(self):
        fr_text = 'Avec sa fille'
        en_text = 'With his daughter'

        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'avec sa fille', 'with his daughter')

    def test_word_disambiguation_from_corpus_mais_elle(self):
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

    def _verify(self, translator, source_text, expected_translation):
        self.assertTrue(translator.translate(source_text) == expected_translation)

    def _new_translator(self, fr_text, en_text, english_model):
        translation_model = FrEnTranslator()
        translation_model.learn_from_text(fr_text, en_text)
        return Translator(translation_model, english_model)

if __name__ == '__main__':
    unittest.main()
