'''
Generative model of English based on a corpus
'''
from nltk.corpus import gutenberg
from nltk import ngrams
from numpy.random import choice
import math

class EnglishModel(object):
    '''Generative model of English'''
    def __init__(self):
        self.freq_1gram = 0
        self.model_1gram = {}
        self.model_2gram = {}
        self.learn_english()

    def summary(self):
        print "seen " + str(self.freq_1gram) + " words."
        print "seen " + str(len(self.model_1gram.keys())) + " unique words."

        p_she = self.probability('she')
        p_hoped = self.probability('hoped')
        p_hoped_given_she = self.probability('hoped', 'she')
        print 'p(she)= ' + str(p_she)
        print 'p(hoped)= ' + str(p_hoped)
        print 'p(hoped | she)= ' + str(p_hoped_given_she)
        print 'p(she hoped) = p(hoped|she)*p(she) = ' + str(p_hoped_given_she * p_she)

    def learn_english(self):
        '''
        Learn unigrams and bigrams from the English corpus
        '''
        texts = []
        texts.append(gutenberg.words('austen-emma.txt'))
        texts.append(gutenberg.words('austen-persuasion.txt'))
        texts.append(gutenberg.words('austen-sense.txt'))
        texts.append(gutenberg.words('chesterton-thursday.txt'))
        texts.append(gutenberg.words('chesterton-brown.txt'))
        texts.append(gutenberg.words('whitman-leaves.txt'))
        texts.append(gutenberg.words('melville-moby_dick.txt'))

        for text in texts:
            self.learn_1grams(text)
            self.learn_2grams([gram for gram in ngrams(text, 2)])

        self.normalize_n1()
        self.normalize_n2()

    def normalize_n1(self):
        '''Normalize all probabilities in the unigram model

        Turns the frequencies into probabilities that sum to 1.0

        Results in a dict such that unigram_model['brother'] = p('brother')
        '''
        for j in self.model_1gram.keys():
            self.model_1gram[j] = float(self.model_1gram[j])/self.freq_1gram

    def normalize_n2(self):
        '''Normalize all probabilities in the bigram model

        Turns the frequencies into probabilities such that
        the probabilities of bigram_model[word] sum to 1.0

        The result is that bigram_model['her']['brother'] = p('brother'|'her')
        '''
        for k1 in self.model_2gram.keys():
            k1_total = 0
            for k2 in self.model_2gram[k1].keys():
                k1_total += self.model_2gram[k1][k2]
            for k2 in self.model_2gram[k1].keys():
                self.model_2gram[k1][k2] = float(self.model_2gram[k1][k2])/k1_total

    def learn_1grams(self, sentence_words):
        for word in sentence_words:
            if self.model_1gram.get(word) == None:
                self.model_1gram[word] = 0
            self.model_1gram[word] += 1.0
            self.freq_1gram += 1.0

    def learn_2grams(self, list_of_2grams):
        for bigram in list_of_2grams:
            w1, w2 = bigram[0], bigram[1]
            if self.model_2gram.get(w1) == None:
                self.model_2gram[w1] = {}
            if self.model_2gram[w1].get(w2) == None:
                self.model_2gram[w1][w2] = 0
            self.model_2gram[w1][w2] += 1.0

    def condition_on(self, word):
        this_dict = self.model_2gram[word]
        items = []
        probs = []
        for key in this_dict.keys():
            items.append(key)
            probs.append(this_dict[key])
        return items, probs

    def produce(self, num_tokens):
        items = []
        probs = []
        for key in self.model_1gram.keys():
            items.append(key)
            probs.append(self.model_1gram[key])

        lastw = ''
        production = []
        for i in range(num_tokens):
            if lastw == '':
                res = choice(items, p=probs)
                lastw = res
            else:
                items, probs = self.condition_on(lastw)
                res = choice(items, p=probs)
                lastw = res
            production.append(res)
        return ' '.join(production)

    def probability_nocond(self, word):
        '''
        Return the probability of the word occuring.

        The probability shall never be zero and the probability
        of a word that has never been seen is one third of the reciprocal
        of the number of words that have been seen.
        '''
        prob = self.model_1gram.get(word)
        if prob == None:
            return 0.33/self.freq_1gram
        return prob

    def probability(self, word, given=''):
        '''
        Return the probability of the word occuring given the previous word

        The probability shall never be zero
        '''
        if given == '':
            return self.probability_nocond(word)

        pword = self.probability_nocond(word)
        if self.model_2gram.get(given) == None:
            return pword
        else:
            givenp = self.model_2gram[given].get(word)
            if givenp == None:
                return 0.33 / (1 + len(self.model_2gram[given].keys()))
            return givenp

    def perplexity(self, sentence_words):
        '''calculate the perplexity of a sentence'''
        perplexity_score = 0
        lastword = ''
        for word in sentence_words:
            perplexity_score += math.log(self.probability(word, lastword), 2)
            lastword = word
        return -1*perplexity_score

    def avg_perplexity(self, sentence_words):
        '''Return the average perplexiy of a sentence

        Returns the perplexity of the sentence divided by the number of
        tokens in the sentence.
        '''
        length = len(sentence_words)
        return self.perplexity(sentence_words)/length

if __name__ == '__main__':
    model = EnglishModel()
    model.summary()
