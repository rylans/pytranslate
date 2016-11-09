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
        p_much_more = self.english.probability('more', 'much')
        p_more_much = self.english.probability('much', 'more')
        self.assertTrue(p_much_more > p_more_much)

    def test_word_order_probability2(self):
        p_pretty_little = self.english.probability('little', 'pretty')
        p_little_pretty = self.english.probability('pretty', 'little')
        self.assertTrue(p_pretty_little > p_little_pretty)

    def test_word_order_probability3(self):
        p_his_wife = self.english.probability('wife', 'his')
        p_wife_his = self.english.probability('his', 'wife')
        self.assertTrue(p_his_wife > p_wife_his)

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

    def test_perplexity_reduced_with_better_grammar2(self):
        px_said_the_woman = self.english.perplexity(['said', 'the', 'woman'])
        px_the_woman_said = self.english.perplexity(['the', 'woman', 'said'])
        px_the_said_woman = self.english.perplexity(['the', 'said', 'woman'])
        self.assertTrue(px_the_said_woman > px_said_the_woman)
        self.assertTrue(px_the_said_woman > px_the_woman_said)

    def test_perplexity_reduced_with_frequency1(self):
        px_his_wife = self.english.perplexity(['his', 'wife'])
        px_her_wife = self.english.perplexity(['her', 'wife'])
        self.assertTrue(px_her_wife > px_his_wife)

    def test_average_perplexity_reduces(self):
        px_we_agreed_to = self.english.avg_perplexity(['we', 'agreed', 'to'])
        px_we_to = self.english.avg_perplexity(['we', 'to'])
        self.assertTrue(px_we_to > px_we_agreed_to)

if __name__ == '__main__':
    unittest.main()
