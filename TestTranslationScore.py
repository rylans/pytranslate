import unittest

from TranslationScore import TranslationScore

class TestFrEnTranslator(unittest.TestCase):
    def test_perfect_translation_zero_words(self):
        self.assertTrue(TranslationScore().of('', '') == 1.0)

    def test_perfect_translation_one_word(self):
        self.assertTrue(TranslationScore().of('hello', 'hello') == 1.0)

    def test_perfect_translation_two_words(self):
        self.assertTrue(TranslationScore().of('hello world', 'hello world') == 1.0)

    def test_perfect_translation_two_words_bad_order(self):
        self.assertTrue(TranslationScore().of('world hello', 'hello world') == 1.0)

    def test_translation_zero_words_in_common(self):
        self.assertTrue(TranslationScore().of('hello', 'goodbye') == 0.0)

    def test_translation_one_word_in_common(self):
        self.assertTrue(TranslationScore().of('oh hello', 'oh goodbye') == 0.25)

    def test_translation_one_word_in_common_actual_longer(self):
        self.assertTrue(TranslationScore().of('oh hello one two', 'oh goodbye') == 0.1875)

    def test_translation_one_word_in_common_expected_longer(self):
        self.assertTrue(TranslationScore().of('oh hello', 'oh goodbye one two') == 0.125)

    def test_translation_three_words_in_common_of_five(self):
        self.assertTrue(TranslationScore().of('one two three go here', 'three two one come there') == 0.36)

if __name__ == '__main__':
    unittest.main()
