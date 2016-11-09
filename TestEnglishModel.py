import unittest

from EnglishModel import EnglishModel

class TestEnglishModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.english = EnglishModel()

    def test_probability_greater_than_zero(self):
        self.assertTrue(self.english.probability('never_occursABC123') > 0)

    def test_that_the_is_probable(self):
        p_the = self.english.probability('the')
        p_danger = self.english.probability('danger')
        self.assertTrue(p_the > p_danger)

    def test_that_existing_word_is_more_probable(self):
        p_over = self.english.probability('over')
        p_none = self.english.probability('never_occursABC123')
        self.assertTrue(p_over > p_none)

    def test_conditional_probability_nonzero(self):
        p_asdf_qwer = self.english.probability('qwer', 'asdf')
        self.assertTrue(p_asdf_qwer > 0)

    def test_word_order_probability1(self):
        p_on_horseback = self.english.probability('horseback', 'on')
        p_horseback_on = self.english.probability('on', 'horseback')
        self.assertTrue(p_on_horseback > p_horseback_on)

    def test_word_order_probability2(self):
        p_pretty_little = self.english.probability('little', 'pretty')
        p_little_pretty = self.english.probability('pretty', 'little')
        self.assertTrue(p_pretty_little > p_little_pretty)

    def test_perplexity_score_increases(self):
        px_I = self.english.perplexity(['I'])
        px_I_declare = self.english.perplexity(['I', 'declare'])
        self.assertTrue(px_I_declare > px_I)

    def test_perlexity_reduced_with_better_grammar(self):
        px_I_declare_that = self.english.perplexity(['I', 'declare', 'that'])
        px_that_I_declare = self.english.perplexity(['that', 'I', 'declare'])
        px_declare_I_that = self.english.perplexity(['declare', 'I', 'that'])
        self.assertTrue(px_that_I_declare < px_declare_I_that)
        self.assertTrue(px_I_declare_that < px_that_I_declare)

if __name__ == '__main__':
    unittest.main()
