# -*- coding: UTF-8 -*-
'''French to English Translator'''

from nltk.align import AlignedSent
from nltk.align import IBMModel2
from EnglishModel import EnglishModel

class FrEnTranslator(object):
    '''Translation module from French to English'''
    def __init__(self, bitext_file_name):
        self.fr_en_dict = {}
        self.target_words = {}
        self.src_words = {}

        self.learn_all(bitext_file_name)
        self.english = EnglishModel(['austen-emma.txt'])

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

    def learn_all(self, filename):
        '''Learn lexicon from list of bilingual texts'''
        self.learn(filename)
        self.norm_source_words()
        self.norm_target_words()

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
        self.ibm2 = IBMModel2(bitext, 2)
        '''
        print ibm2.translation_table
        print ibm2.translation_table['avec']
        print ibm2.translation_table['moi']
        '''

    def ws(self, source):
        return [w.lower() for w in source.split(' ')[1:]]

    def learn_aligned_sentence(self, target, source):
        source_words = [w.lower() for w in source.split(' ')[1:-1]]
        target_words = [w.lower() for w in target.split(' ')[1:-1]]

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
        if self.fr_en_dict.get(src_word) == None:
            return ['[no-translation]']

        candidates = []
        for trg_word in self.fr_en_dict[src_word]:
            p_trg_given_src = self.translation_probability(trg_word, src_word)
            candidates.append((p_trg_given_src, trg_word))
        sorted_candidates = sorted(candidates)[::-1]
        if top == 1:
            return sorted_candidates[0][1]
        return [k[1] for k in sorted_candidates[:top]]

    def translation_probability(self, trg_word, src_word):
        '''Compute probability of target word given source word'''
        if self.fr_en_dict.get(src_word) == None:
            return 0
        if self.fr_en_dict[src_word].get(trg_word) == None:
            return 0
        return self.ibm2.translation_table[src_word][trg_word] * self.src_words[src_word]

    def translate(self, source_sentence):
        '''Translate source sentence to English'''
        src_words = source_sentence.split(' ')
        local_dict = {}
        for src_word in src_words:
            local_dict[src_word] = self.translate_word(src_word, 8)
            print src_word + " " + str(local_dict[src_word])

        possible_translation = []
        for src_word in src_words:
            possible_translation.append(local_dict[src_word][0])


        px1 = self.english.avg_perplexity(possible_translation)
        px2 = px1
        improvement = 1
        alternate = ' '.join(possible_translation)
        while (improvement > 0.03):
            ix = self.most_perplexing(possible_translation)
            print improvement, ix
            if ix == 0:
                break
            try:
                alternate = ' '.join(possible_translation)
                possible_translation[ix] = self.translate_word(src_words[ix], 2)[1]
            except IndexError:
                return alternate

            px1 = px2
            px2 = self.english.avg_perplexity(possible_translation)
            improvement = px1 - px2
            if improvement < 0:
                return alternate

        return ' '.join(possible_translation)

    def argmin(self, lst):
        minval = lst[0]
        minix = 0
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

        print px_array
        return self.argmin(px_array)

def demo():
    '''
    translator = FrEnTranslator('texts/sample_en_fr.txt')

    phrase2 = "corruption de fonctionnaires avait un avis de notre femme ."
    print translator.translate(phrase2)
    print

    phrase3 = "sa mère avait les choix et elle avait la fille ."
    print translator.translate(phrase3)
    '''

    translator = FrEnTranslator('texts/test_en_fr.txt')
    print translator.translate('elles dansent et elles sont morts .')

if __name__ == '__main__':
    demo()
