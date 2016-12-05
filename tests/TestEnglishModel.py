import unittest

from pytranslate.english_model import EnglishModel

class TestEnglishModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.english = EnglishModel(['austen-emma.txt', 'chesterton-thursday.txt'])
        self.udhr_article3 = 'everyone has the right to life , liberty , and person .'.split()
        self.udhr_article4 = 'no one shall be held in slavery or servitude .'.split()
        self.udhr_article5 = 'no one shall be subjected to torture or to cruel , inhuman or degrading treatment .'.split()

    def test_probability_greater_than_zero(self):
        self.assertTrue(self.english.probability('never_occursABC123') > 0)

    def test_that_the_is_probable(self):
        p_the = self.english.probability('the')
        p_danger = self.english.probability('danger')
        self.assertTrue(p_the > p_danger)

    def test_that_existing_word_is_more_probable(self):
        p_over = self.english.probability('over')
        p_none = self.english.probability('never_occursABC123')
        self.assertTrue(p_none > 0)
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

    def test_average_perplexity_reduces1(self):
        px_we_agreed_to = self.english.avg_perplexity(['we', 'agreed', 'to'])
        px_we_to = self.english.avg_perplexity(['we', 'to'])
        self.assertTrue(px_we_to > px_we_agreed_to)

    def test_average_perplexity_reduces2(self):
        px_on_top_of = self.english.avg_perplexity(['on', 'top', 'of'])
        px_on_of = self.english.avg_perplexity(['on', 'of'])
        self.assertTrue(px_on_of > px_on_top_of)

    def test_average_perplexity_on_word_deletions_article3(self):
        self.given_text_assert_average_perplexity_on_word_deletions(self.udhr_article3, self.english)

    def test_average_perplexity_on_word_deletions_article4(self):
        self.given_text_assert_average_perplexity_on_word_deletions(self.udhr_article4, self.english)

    def test_average_perplexity_on_word_deletions_article5(self):
        self.given_text_assert_average_perplexity_on_word_deletions(self.udhr_article5, self.english)

    def given_text_assert_average_perplexity_on_word_deletions(self, text, eng_model):
        px_text = eng_model.avg_perplexity(text)
        one_drop_sentences = self.drop_one_word(text)

        px_count = 0
        for sen in one_drop_sentences:
            px_count += eng_model.avg_perplexity(sen)
        px_total_avg = px_count / len(one_drop_sentences)

        self.assertTrue(px_total_avg > px_text)

    def drop_one_word(self, sentence):
        '''Return sentences with one word removed

        Args:
            sentence (list): The list of words in sentence order

        Returns:
            list: A list of partial sentences
        '''
        one_drop_sentences = []
        for k in range(len(sentence) - 1):
            sen = sentence[:k+1] + sentence[k+2:]
            one_drop_sentences.append(sen)
        return one_drop_sentences

