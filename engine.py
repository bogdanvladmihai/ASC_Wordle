from math import log2

from dataSource import DataSource
from game import compareWords

FIRST = "TAREI"

class Engine:
    dataSource = DataSource()

    def __init__(self):
        self.guesses = 0
        self.lastHash = -1
        self.possibleWords = Engine.dataSource.words
        self.secondChoice = Engine.dataSource.second

    def chooseWord(self):
        if self.guesses == 0:
            return FIRST
        elif self.guesses == 1:
            return self.secondChoice[self.lastHash]
        elif len(self.possibleWords) == 1:
            return self.possibleWords[0]
        elif len(self.possibleWords) == 0:
            return None
    

        # file = open("output.txt", "w")

        # entropies = []
        # index = 0
        best_word = "aaaaa"
        max = 0
        for word in self.possibleWords:
            entropy = self.computeEntropy(word)
            if max < entropy:
                max = entropy
                best_word = word

        return best_word

        # entropies.sort(key=lambda x: x[1], reverse=True)

        # for pair in entropies:
        #     print(pair, file=file)
        #
        # print(entropies)

    def computeEntropy(self, word):
        buckets = [0] * 243
        for secretWord in self.possibleWords:
            buckets[compareWords(secretWord, word)] += 1

        entropy = 0
        for count in buckets:
            if count == 0:
                continue
            p = count / len(self.possibleWords)
            entropy = entropy + p * (-log2(p))

        return entropy

    def updateWords(self, word, value):
        self.guesses += 1
        self.lastHash = value

        new_list = []
        for secretWord in self.possibleWords:
            if compareWords(secretWord, word) == value:
                new_list.append(secretWord)
        self.possibleWords = new_list
