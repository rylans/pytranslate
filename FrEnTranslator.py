# -*- coding: UTF-8 -*-
'''French to English Translator'''

from nltk.align import AlignedSent
from nltk.align import IBMModel2
from EnglishModel import EnglishModel

class FrEnTranslator(object):
    '''Translation module from French to English'''
    def __init__(self):
        self.english = EnglishModel(['austen-emma.txt'])
        self.translation_table = None
        self.fr_en_dict = {}
        self.target_words = {}
        self.src_words = {}

        '''
        if fr_file != '' and en_file != '':
            fr_lines, en_lines = self.aligned_text_from_files(fr_file, en_file)
            self.learn_aligned_text(fr_lines, en_lines)
        else:
            self.learn_all(bitext_file_name)
            '''

    def after_learn(self):
        self.norm_source_words()
        self.norm_target_words()

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

    def norm_target_words(self):
        '''Normalize source words from frequencies to probabilities'''
        src_word_sum = 0
        for src_word in self.target_words.keys():
            src_word_sum += self.target_words[src_word]

        for src_word in self.target_words.keys():
            self.target_words[src_word] = self.target_words[src_word]/float(src_word_sum)

    def invert_targets(self):
        '''Invert target words

        Result is that inv_target_frequency['the'] = 1.0/(1+freq('the'))
        '''
        for trg_word in self.target_words.keys():
            self.inv_target_frequency[trg_word] = 1.0/(1+self.target_words[trg_word])

    '''
    def learn_all(self, filename):
        self.learn(filename)
        '''

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

    '''
    def learn(self, filename):
        bitext = []
        en_line = ''
        fr_line = ''
        with open(filename, 'r') as open_file:
            for line in open_file.readlines():
                if "EN " in line:
                    en_line = line
                if "FR " in line:
                    fr_line = line
                if en_line != '' and fr_line != '':
                    bitext.append(AlignedSent(self.ws(fr_line), self.ws(en_line)))
                    self.learn_aligned_sentence(en_line, fr_line)
                    en_line, fr_line = '', ''
        self.ibm2 = IBMModel2(bitext, 5)

    def ws(self, source):
        return [w.lower() for w in source.split(' ')[1:]]
        '''

    def learn_aligned_sentence(self, target, source):
        source_words = [w for w in self.preprocess(source)]
        target_words = [w for w in self.preprocess(target)]

        #source_words = [w.lower() for w in source.split(' ')]
        #target_words = [w.lower() for w in target.split(' ')]

        for source_word in source_words:
            for target_word in target_words:
                if self.fr_en_dict.get(source_word) == None:
                    self.fr_en_dict[source_word] = {}
                if self.fr_en_dict[source_word].get(target_word) == None:
                    self.fr_en_dict[source_word][target_word] = 0
                self.fr_en_dict[source_word][target_word] += 1

        for target_word in target_words:
            if self.target_words.get(target_word) == None:
                self.target_words[target_word] = 0
            self.target_words[target_word] += 1

        for src_word in source_words:
            if self.src_words.get(src_word) == None:
                self.src_words[src_word] = 0
            self.src_words[src_word] += 1

    def translate_word(self, src_word, top=1):
        if src_word == '.':
            return ['.']
        if self.translation_table.get(src_word) == None:
            return ['[no-translation]']

        candidates = []
        for trg_word in self.translation_table[src_word]:
            p_trg_given_src = self.translation_probability(trg_word, src_word)
            candidates.append((p_trg_given_src, trg_word))
        sorted_candidates = [c for c in sorted(candidates)[::-1] if c[0] > 0]
        if top == 1:
            return sorted_candidates[0][1]
        return [k[1] for k in sorted_candidates[:top]]

    def translation_probability(self, trg_word, src_word):
        '''Compute probability of target word given source word'''
        if self.fr_en_dict.get(src_word) == None:
            return 0
        if self.fr_en_dict[src_word].get(trg_word) == None:
            return 0
        return self.translation_table[src_word][trg_word] * self.src_words[src_word]

    def translate(self, source_sentence):
        '''Translate source sentence to English'''
        if self.translation_table == None:
            raise Exception("Unable to translate before learning")
        src_words = self.preprocess(source_sentence)
        local_dict = {}
        for src_word in src_words:
            translation_options = self.translate_word(src_word, 8)
            local_dict[src_word] = translation_options

        possible_translation = []
        for src_word in src_words:
            try:
                possible_translation.append(local_dict[src_word][0])
            except IndexError:
                possible_translation.append('[none]')

        if not self.english:
            return ' '.join(possible_translation)
        px1 = self.english.avg_perplexity(possible_translation)
        px2 = px1
        improvement = 1
        alternate = ' '.join(possible_translation)
        while (improvement > 0.03):
            ix = self.most_perplexing(possible_translation)
            if ix == None:
                break

            alternate = ' '.join(possible_translation)
            dozen = self.translate_word(src_words[ix], 3)
            if len(dozen) < 2:
                return alternate
            else:
                orig = possible_translation[ix]
                for word in dozen:
                    possible_translation[ix] = word
                    px = self.english.avg_perplexity(possible_translation)
                    if (px1 - px) > 0.2:
                        return ' '.join(possible_translation)
                possible_translation[ix] = orig

            px1 = px2
            px2 = self.english.avg_perplexity(possible_translation)
            improvement = px1 - px2
            if improvement < 0:
                return alternate

        return ' '.join(possible_translation)

    def argmin(self, lst):
        minix = None
        minval = 0
        for i in range(len(lst)):
            if lst[i] < minval:
                minval = lst[i]
                minix = i
        return minix

    def most_perplexing(self, sentence):
        '''Compute the index of the sentence that increases perplexity the most'''
        interesting_index = len(sentence) - 1

        px_array = []
        last_px = 0
        for k in range(len(sentence) - 1):
            sen = sentence[:k+1]
            px = self.english.avg_perplexity(sen)
            marginal = px - last_px
            if marginal > 0.02:
                interesting_index = k
            last_px = px
            px_array.append(marginal)

        return self.argmin(px_array)

def demo():
    translator = FrEnTranslator()
    translator.learn_from_file('texts/europarl-sample.fr-en.fr', 'texts/europarl-sample.fr-en.en')
    print translator.translate('Je vous invite à vous lever pour cette minute de silence.')
    print translator.translate("Madame la Présidente, c'est une motion de procédure.")
    print translator.translate("Et tout ceci dans le respect des principes que nous avons toujours soutenus.")

    fr_side = '''elle a un chien
il a un chat
elle dit
un taureau'''

    en_side = '''she has a dog
he has a cat
she says
a bull'''

    translator = FrEnTranslator()
    translator.learn_from_text(fr_side, en_side)
    print translator.translate('il a un chien')

if __name__ == '__main__':
    demo()
