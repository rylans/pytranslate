# -*- coding: UTF-8 -*-
'''French to English Translator'''

class FrEnTranslator(object):
    def __init__(self):
        '''
        fr_en_dict['maison']['house'] = 0.63
        fr_en_dict['maison']['the'] = 0.02
        '''
        self.fr_en_dict = {}
        self.target_words = {}
        self.src_words = {}
        self.inv_target_frequency = {}

        self.learn_all([])

    def norm(self):
        '''Normalize fr_en_dict from frequencies to probabilities'''
        for src_word in self.fr_en_dict.keys():
            src_word_sum = 0
            for trg_word in self.fr_en_dict[src_word].keys():
                src_word_sum += self.fr_en_dict[src_word][trg_word]

            for trg_word in self.fr_en_dict[src_word].keys():
                self.fr_en_dict[src_word][trg_word] = self.fr_en_dict[src_word][trg_word]/float(src_word_sum)

    def invert_targets(self):
        '''Invert target words

        Result is that inv_target_frequency['the'] = 1.0/(1+freq('the'))
        '''
        for trg_word in self.target_words.keys():
            self.inv_target_frequency[trg_word] = 1.0/(1+self.target_words[trg_word])

    def learn_all(self, filenames):
        '''Learn lexicon from list of bilingual texts'''
        #TODO read filenames
        self.learn('texts/sample_en_fr.txt')
        self.norm()
        self.invert_targets()

    def learn(self, filename):
        en_line = ''
        fr_line = ''
        with open(filename, 'r') as open_file:
            for line in open_file.readlines():
                if "EN " in line:
                    en_line = line
                if "FR " in line:
                    fr_line = line
                if en_line != '' and fr_line != '':
                    self.learn_aligned_sentence(en_line, fr_line)
                    en_line, fr_line = '', ''

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
            return '[no-translation]'

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
        return self.fr_en_dict[src_word][trg_word] * self.inv_target_frequency[trg_word]

def demo():
    translator = FrEnTranslator()

    '''
    sen = 'soit de provoquer ou de faciliter la perpétration d’une infraction ,'.split(' ')
    for word in sen:
        print word + " " + str(translator.translate_word(word, 8))

    '''
    sen2 = "personne avec l’intention de offre qui .".split()
    for word in sen2:
        print word + " " + str(translator.translate_word(word, 8))

    '''
    for src_word in translator.src_words:
        if translator.src_words[src_word] > 2:
            print src_word
    '''

if __name__ == '__main__':
    demo()
