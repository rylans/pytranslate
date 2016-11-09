'''
Generative model of English based on a corpus
'''
from nltk.corpus import gutenberg
from nltk import ngrams
from collections import defaultdict

class EnglishModel(object):
    def __init__(self):
        self.model_1gram = defaultdict(lambda: 1.0)
        self.model_2gram = defaultdict(lambda: [])
        self.model_3gram = defaultdict(lambda: [])
        self.learn_english()

    def learn_english(self):
        emma = gutenberg.words('austen-emma.txt')

        emma_samples = []
        emma_samples.append(emma[186:261])
        emma_samples.append(emma[261:308])
        emma_samples.append(emma[308:332])

        for text in emma_samples:
            self.learn_1grams(text)
            self.learn_2grams([gram for gram in ngrams(text, 2)])
            self.learn_3grams([gram for gram in ngrams(text, 3)])

    def learn_1grams(self, sentence_words):
        for word in sentence_words:
            self.model_1gram[word] += 1

    def learn_2grams(self, list_of_2grams):
        for bigram in list_of_2grams:
            self.model_2gram[bigram[0]] += [bigram[1]]

    def learn_3grams(self, list_of_3grams):
        for trigram in list_of_3grams:
            self.model_3gram[trigram[:2]] += [trigram[2]]

    def probability(self, word):
        '''
        Return the probability of the word occuring.
        Probability shall never be zero
        '''
        total_occur = 0
        for key in self.model_1gram.keys():
            total_occur += self.model_1gram[key]
        freq = self.model_1gram[word]
        return float(freq)/total_occur

if __name__ == '__main__':
    model = EnglishModel()

    print model.probability('the')
    print model.probability('Taylor')
    print model.probability('a3nf')
