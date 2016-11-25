# -*- coding: UTF-8 -*-
'''target language to target language abstract translation model'''

from nltk.align import AlignedSent
from nltk.align import IBMModel3

from text_utils import preprocess

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
        self.fertility_table = None
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

    def aligned_text_from_strings(self, fr_string, en_string):
        '''Get aligned sentences from both texts

        Returns a 2-tuple of lists of strings
        '''
        fr_lines = fr_string.split('\n')
        en_lines = en_string.split('\n')
        fr_lines = [q for q in fr_lines if q != '']
        en_lines = [q for q in en_lines if q != '']
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
        '''Learn from IBM-aligned model of lists of lines of both languages'''
        bitext = []
        bitext_flip = []
        for pair in zip(fr_lines, en_lines):
            pp0 = preprocess(pair[0])
            pp1 = preprocess(pair[1])
            if len(pp0) == 0 or len(pp1) == 0:
                continue
            if pp0[0] == '' or pp0[1] == '':
                continue
            bitext.append(AlignedSent(pp0, pp1))
            bitext_flip.append(AlignedSent(pp1, pp0))
            self.learn_aligned_sentence(pair[1], pair[0])
        ibm = IBMModel3(bitext, 5)
        self.translation_table = ibm.translation_table

        ibm_flip = IBMModel3(bitext_flip, 5)
        self.fertility_table = ibm_flip.fertility_table

    def learn_aligned_sentence(self, target, source):
        source_words = [w for w in preprocess(source)]
        target_words = [w for w in preprocess(target)]

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

    def fertility(self, src_word):
        '''Return the fertility table's row for a given word

        Args:
            src_word (string): The word in the source text

        Returns:
            tuple: (0.11, 0.5, 0.39)
        if word has not been seen, then (1/3, 1/3, 1/3)
        '''
        f0, f1, f2 = self.fertility_table[0][src_word], \
                self.fertility_table[1][src_word], \
                self.fertility_table[2][src_word]
        total = float(f0 + f1 + f2)
        return (f0/total, f1/total, f2/total)

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
    trx = TranslationModel()
    fr_tx= '''elle va aller
elle est rouge
elle veut aller avec moi
il est mon ami
un chien veut manger le chat
un ami
le chien
elle va manger avec toi
elles sont les filles
elles sont avec moi'''
    en_tx = '''she wants to go
she is red
she wants to go with me
he is my friend
a dog wants to eat the cat
a friend
the dog
she is going to eat with you
they are girls
they are with me'''

    trx.learn_from_text(fr_tx, en_tx)
    #trx.learn_from_text('elle va aller\nelle est rouge', 'she wants to go\nshe is red')
    print trx.translate_word('elle', 5, True)
    print trx.translate_word('va', 5, True)
    print trx.translate_word('aller', 5, True)
    print trx.translate_word('manger', 5, True)
    print trx.translate_word('ami', 5, True)
    print trx.fertility('manger')
    print trx.fertility('va')
    print trx.fertility('aller')
