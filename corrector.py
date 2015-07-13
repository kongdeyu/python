#coding:utf-8


import collections
import re


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class Corrector(object):

    model = collections.defaultdict(lambda: 1)

    def train(self, sample_file):
        with open(sample_file, 'r') as f:
            features = re.findall(r'[a-z]+', f.read().lower())
            for item in features:
                Corrector.model[item] += 1

    def correct(self, word):
        candidate = (self.__known([word])
                or self.__known(self.__edit_distance1(word))
                or self.__edit_distance2_known(word)
                or [word])
        return max(candidate, key=lambda w: Corrector.model[w])

    # private method
    def __edit_distance1(self, word):
        length = len(word)
        return set([word[0: i] + word[i + 1:] for i in xrange(length)] +  # deletion
                [word[0: i] + word[i + 1] + word[i] + word[i + 2:] for i in xrange(length - 1)] +  # transposition
                [word[0: i] + ch + word[i + 1:] for i in xrange(length) for ch in ALPHABET] +  # alteration
                [word[0: i] + ch + word[i:] for i in xrange(length) for ch in ALPHABET])  # insertion

    def __edit_distance2(self, word):
        return set(w2 for w1 in self.__edit_distance1(word)
                for w2 in self.__edit_distance1(w1))

    def __edit_distance2_known(self, word):
        return set(w2 for w1 in self.__edit_distance1(word)
                for w2 in self.__edit_distance1(w1) if w2 in Corrector.model)

    def __known(self, words):
        return set(w for w in words if w in Corrector.model)


def Error(Exception):
    pass
