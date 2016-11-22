# -*- coding: UTF-8 -*-
'''target language to target language abstract translation model'''

from nltk.align import AlignedSent
from nltk.align import IBMModel2

class TranslationModel(object):
    '''Translation module from French to English

    P(a|b) = p(b|a) * p(a) [p(b) ignored since we're maximizing]

    French -> English
    Probability of three english words given 3 french words (bigram model):
    P(e1 e2 e3 | f1 f2 f3)
        = p(f1 f2 f3 | e1 e2 e3) * p(e1 e2 e3)
        = p(f1 f2 f3 | e...) * p(e3|e2) * p(e2|e1) * p(e1) [markov assumption]
        = p(f1 | e1) * p(f2 | e2) * p(f3 | e3) * p(e3 | e2) * p(e2 | e1) * p(e1)
        = t_3

    p(e1 e2 e3 e4 | f1 f2 f3 f4) = t_3 * p(f4 | e4) * p(e4 | e3)
    '''
    def __init__(self):
        self.translation_table = None
        self.fr_en_dict = {}
        self.src_words = {}

    def after_learn(self):
        self.norm_source_words()

    def learn_from_file(self, fr_file, en_file):
        '''Train the translation model on these two files'''
        if fr_file == '' or en_file == '':
            raise Exception("nothing to learn")
        fr_lines, en_lines = self.aligned_text_from_files(fr_file, en_file)
        self.learn_aligned_text(fr_lines, en_lines)
        self.after_learn()

    def learn_from_text(self, fr_text, en_text):
        '''Train the translation model on these two text strings'''
        if fr_text == '' or en_text == '':
            raise Exception("nothing to learn")
        fr_lines, en_lines = self.aligned_text_from_strings(fr_text, en_text)
        self.learn_aligned_text(fr_lines, en_lines)
        self.after_learn()

    def norm_source_words(self):
        '''Normalize source words from frequencies to probabilities'''
        src_word_sum = 0
        for src_word in self.src_words.keys():
            src_word_sum += self.src_words[src_word]

        for src_word in self.src_words.keys():
            self.src_words[src_word] = self.src_words[src_word]/float(src_word_sum)

    def preprocess(self, line):
        '''Process a line into a list of tokens'''
        no_newline = line.replace('\n', '')
        lowline = no_newline.lower()
        comma_sep = lowline.replace(',', ' ,')
        apostrophe_sep = comma_sep.replace("'", "' ")
        period_sep = apostrophe_sep.replace('.', ' .')
        hyphen_sep = period_sep.replace('-', ' ')
        question_sep = hyphen_sep.replace('?', ' ?')
        return question_sep.split(' ')

    def aligned_text_from_strings(self, fr_string, en_string):
        '''Get aligned sentences from both texts

        Returns a 2-tuple of lists of strings
        '''
        fr_lines = fr_string.split('\n')
        en_lines = en_string.split('\n')
        assert len(fr_lines) == len(en_lines)
        return (fr_lines, en_lines)

    def aligned_text_from_files(self, fr_file, en_file):
        fr_lines = []
        en_lines = []
        with open(fr_file, 'r') as open_fr_file:
            for line in open_fr_file.readlines():
                fr_lines.append(line)

        with open(en_file, 'r') as open_en_file:
            for line in open_en_file.readlines():
                en_lines.append(line)

        assert len(fr_lines) == len(en_lines)

        return (fr_lines, en_lines)

    def learn_aligned_text(self, fr_lines, en_lines):
        '''Learn from IBM2-aligned model of lists of lines of both languages'''
        bitext = []
        for pair in zip(fr_lines, en_lines):
            bitext.append(AlignedSent(self.preprocess(pair[0]), self.preprocess(pair[1])))
            self.learn_aligned_sentence(pair[1], pair[0])
        ibm2 = IBMModel2(bitext, 5)
        self.translation_table = ibm2.translation_table

    def learn_aligned_sentence(self, target, source):
        source_words = [w for w in self.preprocess(source)]
        target_words = [w for w in self.preprocess(target)]

        for source_word in source_words:
            for target_word in target_words:
                if self.fr_en_dict.get(source_word) == None:
                    self.fr_en_dict[source_word] = {}
                if self.fr_en_dict[source_word].get(target_word) == None:
                    self.fr_en_dict[source_word][target_word] = 0
                self.fr_en_dict[source_word][target_word] += 1

        for src_word in source_words:
            if self.src_words.get(src_word) == None:
                self.src_words[src_word] = 0
            self.src_words[src_word] += 1

    def translate_word(self, src_word, top=1, with_probs=False):
        if src_word == '.':
            return [(0.025, '.')] #FIXME: fix this
        if self.translation_table.get(src_word) == None:
            return None

        candidates = []
        for trg_word in self.translation_table[src_word]:
            p_trg_given_src = self.translation_probability(trg_word, src_word)
            candidates.append((p_trg_given_src, trg_word))
        sorted_candidates = [c for c in sorted(candidates)[::-1] if c[0] > 0]
        if top == 1:
            return sorted_candidates[0][1]
        if with_probs:
            return sorted_candidates[:top]
        return [k[1] for k in sorted_candidates[:top]]

    def translation_probability(self, trg_word, src_word):
        '''Compute probability of target word given source word'''
        if self.fr_en_dict.get(src_word) == None:
            return 0
        if self.fr_en_dict[src_word].get(trg_word) == None:
            return 0
        return self.translation_table[src_word][trg_word] * self.src_words[src_word]

if __name__ == '__main__':
    trx = FrEnTranslator()
    trx.learn_from_text('elle va aller\nelle est rouge', 'she wants to go\nshe is red')
    print trx.translate_word('elle', 5, True)

