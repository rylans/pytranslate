# -*- coding: UTF-8 -*-
import unittest

from FrEnTranslator import FrEnTranslator

class TestFrEnTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.translator = FrEnTranslator('texts/test_en_fr.txt')

    def test_translate_garcon(self):
        self.verify_translation('garçon', 'boy')

    def test_translate_dansent(self):
        self.verify_translation('dansent', 'dance')

    def test_translate_elles_dansent(self):
        self.verify_full_translation('elles dansent et elles sont morts .', 'they dance and they are dead .')

    def verify_full_translation(self, french, english):
        self.assertTrue(self.translator.translate(french) == english)

    def verify_translation(self, french_word, english_word):
        self.assertTrue(self.translator.translate_word(french_word) == english_word)

if __name__ == '__main__':
    unittest.main()
