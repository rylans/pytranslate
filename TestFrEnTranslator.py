import unittest

from FrEnTranslator import FrEnTranslator

class TestFrEnTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.translator = FrEnTranslator()

    def test_source_il_translations(self):
        p_il_to_he = self.translator.translation_probability('he', 'il')
        self.assertTrue(p_il_to_he > 0)
        p_il_to_she = self.translator.translation_probability('she', 'il')
        self.assertTrue(p_il_to_he > p_il_to_she)
        p_il_to_the = self.translator.translation_probability('the', 'il')
        self.assertTrue(p_il_to_he > p_il_to_the)

    def test_translate_corruption(self):
        self.verify_translation('corruption', 'bribery')

    def test_translate_sur(self):
        self.verify_translation('sur', 'on')

    def test_translate_quatorze(self):
        self.verify_translation('quatorze', 'fourteen')

    def test_translate_sans(self):
        self.verify_translation('sans', 'without')

    def test_translate_sous(self):
        self.verify_translation('sous', 'under')

    def verify_translation(self, french_word, english_word):
        self.assertTrue(self.translator.translate_word(french_word) == english_word)

if __name__ == '__main__':
    unittest.main()
