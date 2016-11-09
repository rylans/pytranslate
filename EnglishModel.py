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
        for j in self.model_1gram.keys():
            self.model_1gram[j] = float(self.model_1gram[j])/self.freq_1gram

    def normalize_n2(self):
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
        '''Learned Bigrams
        So that
            self.model_2gram['when'] =
                {'the': 2.1,
                 'our': 3.0}
        '''
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
        Probability shall never be zero
        '''
        prob = self.model_1gram.get(word)
        if prob == None:
            return 0.33/self.freq_1gram
        return prob

    def probability(self, word, given=''):
        '''
        Return the probability of the word occuring given the given word
        Probability shall never be zero


        p('said'|'she') = model_2gram['she']['said']/p('she') If it exists
                        = p('said') otherwise

        P(A|B) = P(A ^ B)/P(B)

        p('horseback' | 'on') > p('on'| 'horseback')
        '''
        if given == '':
            return self.probability_nocond(word)

        pword = self.probability_nocond(word)
        if self.model_2gram.get(given) == None:
            return pword
        else:
            givenp = self.model_2gram[given].get(word)
            if givenp == None:
                return pword
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
        length = len(sentence_words)
        return self.perplexity(sentence_words)/length

if __name__ == '__main__':
    model = EnglishModel()

    print
    sentence1 = ['his', 'wife', 'said']
    print sentence1
    print model.avg_perplexity(sentence1)

    print
    sentence2 = ['her', 'wife', 'said']
    print sentence2
    print model.avg_perplexity(sentence2)

    print
    sentence3 = ['his', 'wife', 'gone']
    print sentence3
    print model.avg_perplexity(sentence3)

    print model.produce(30)
