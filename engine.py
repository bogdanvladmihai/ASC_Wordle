from math import log2

from dataSource import DataSource
from game import compareWords

FIRST = "TAREI"
LAYERONELIMIT = 500000

class Engine:
    dataSource = DataSource()

    def __init__(self):
        self.guesses = 0
        self.lastHash = -1
        self.words = Engine.dataSource.words
        self.possibleWords = Engine.dataSource.words
        self.secondChoice = Engine.dataSource.second

    def simulate(self, word):
        entropy = 0
        bucket = []
        for i in range(3 ** 5):
            bucket.append([])
        for secretWord in self.words:
            bucket[compareWords(secretWord, word)].append(secretWord)

        for feedbackCode in range(3 ** 5):
            if len(bucket[feedbackCode]) == 0:
                continue
            # 

        return entropy

    def chooseWord(self):
        if self.guesses == 0:
            return FIRST
        elif self.guesses == 1:
            return self.secondChoice[self.lastHash]
        if len(self.possibleWords) == 1:
            return self.possibleWords[0]
        elif len(self.possibleWords) == 0:
            return None
    
        if len(self.possibleWords) <= LAYERONELIMIT:
            l = self.possibleWords
            if len(self.possibleWords) >= 3:
                l = self.words

            best_word = None
            max = 0
            for word in l:
                entropy = self.computeEntropy(word)
                if max < entropy:
                    max = entropy
                    best_word = word

            return best_word
        else:
            entropies = []
            for word in self.words:
                entropies.append([self.computeEntropy(word), word])

            entropies.sort()
            numberOfCandidates = 0
            if len(self.possibleWords) > 1000:
                numberOfCandidates = 100
            elif len(self.possibleWords) >= 50:
                numberOfCandidates = 10
            else:
                numberOfCandidates = 5       
            candidates = entropies[-numberOfCandidates:]

            best = 0
            answer = None
            for candidate in candidates:
                simulationResult = self.simulate(candidate[1])
                if simulationResult > best:
                    best = simulationResult
                    answer = candidate
            
            return answer

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
