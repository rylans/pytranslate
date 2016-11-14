'''French to English Translator'''

class FrEnTranslator(object):
    def __init__(self):
        '''
        fr_en_dict['maison']['house'] = 0.63
        fr_en_dict['maison']['the'] = 0.02
        '''
        self.fr_en_dict = {}
        self.target_words = {}
        self.inv_target_frequency = {}
        self.learn_all([])

    def norm(self):
        '''Normalize fr_en_dict from frequencies to  probabilities'''
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
                if self.target_words.get(target_word) == None:
                    self.target_words[target_word] = 0
                self.target_words[target_word] += 1
        self.fr_en_dict['.']['.'] += 250

    def translate_word(self, src_word):
        max_p = 0
        argmax = ''
        if self.fr_en_dict.get(src_word) == None:
            return '[no-translation]'
        for trg_word in self.fr_en_dict[src_word]:
            p_trg_given_src = self.fr_en_dict[src_word][trg_word] * self.inv_target_frequency[trg_word]
            if p_trg_given_src > max_p:
                max_p = p_trg_given_src
                argmax = trg_word
        return argmax

def demo():
    translator = FrEnTranslator()
    #print translator.target_words
    #print translator.inv_target_frequency
    for w in 'cette femme assise dans le grand fauteuil .'.split(' '):
        print translator.translate_word(w)

if __name__ == '__main__':
    demo()
