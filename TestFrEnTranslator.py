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

if __name__ == '__main__':
    unittest.main()
