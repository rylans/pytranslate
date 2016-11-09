'''
Generative model of English based on a corpus
'''
from nltk.corpus import gutenberg
from nltk import ngrams
from collections import defaultdict

class EnglishModel(object):
    def __init__(self):
        self.model_1gram = defaultdict(lambda: 0.2)
        self.model_2gram = defaultdict(lambda: [])
        self.model_3gram = defaultdict(lambda: 0.2)
        self.learn_english()

    def learn_english(self):
        emma = gutenberg.words('austen-emma.txt')
        emma_sample = emma[186:261]

        self.learn_1grams(emma_sample)
        print self.model_1gram

        self.learn_2grams([gram for gram in ngrams(emma_sample, 2)])
        print self.model_2gram

        trigrams = ngrams(emma_sample, 3)

    def learn_1grams(self, sentence_words):
        for word in sentence_words:
            self.model_1gram[word] += 1

    def learn_2grams(self, list_of_2grams):
        for bigram in list_of_2grams:
            self.model_2gram[bigram[0]] += [bigram[1]]



if __name__ == '__main__':
    model = EnglishModel()


