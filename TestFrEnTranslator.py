# -*- coding: UTF-8 -*-
import unittest

from FrEnTranslator import FrEnTranslator

class TestFrEnTranslator(unittest.TestCase):

    def test_simple_translation(self):
        fr_side = '''il rit
elle dit
il est'''

        en_side = '''he laughs
she says
he is'''

        translator = FrEnTranslator()
        translator.learn_from_text(fr_side, en_side)
        self.verify_full_translation(translator, 'elle rit', 'she laughs')
        self.verify_full_translation(translator, 'il dit', 'he says')

    def test_word_deletion_translation(self):
        fr_side = '''Les deux yeux
    Les parents sont ici
    Ils sont morts
    Dans les deux cas'''

        en_side = '''Both eyes
    The parents are here
    They are dead
    In both cases'''

        translator = FrEnTranslator()
        translator.learn_from_text(fr_side, en_side)
        self.verify_full_translation(translator, 'Les deux sont ici', 'both are here')

    def verify_full_translation(self, translator, french, english):
        self.assertTrue(translator.translate(french) == english)

if __name__ == '__main__':
    unittest.main()
