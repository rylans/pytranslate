import unittest

from EnglishModel import EnglishModel

class TestEnglishModel(unittest.TestCase):
    def test_probability_greater_than_zero(self):
        english = EnglishModel()
        self.assertTrue(english.probability('never_occursABC123') > 0)

    def test_that_the_is_probable(self):
        english = EnglishModel()
        p_the = english.probability('the')
        p_danger = english.probability('danger')
        self.assertTrue(p_the > p_danger)

if __name__ == '__main__':
    unittest.main()
