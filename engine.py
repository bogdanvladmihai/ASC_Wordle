from math import log2
import string

from dataSource import DataSource
from game import compareWords

FIRST = "TUREI"
PRI = 97

class Engine:
    dataSource = DataSource()

    def __init__(self):
        self.guesses = []
        self.words = Engine.dataSource.words
        self.possibleWords = Engine.dataSource.words
        self.secondChoice = Engine.dataSource.second
        self.third = Engine.dataSource.third
        self.freq = Engine.dataSource.freq

        self.possible = set()
        for word in self.words:
            self.possible.add(hash(word))

    def computeSimulationEntropy(self, word, secretWords):
        buckets = [0] * 243
        for secretWord in secretWords:
            buckets[compareWords(secretWord, word)] += 1

        entropy = 0
        for count in buckets:
            if count == 0:
                continue
                
            prob = count / len(secretWords)
            entropy = entropy + prob * (-log2(prob))

        return entropy
        

    def simulate(self, word):
        possible = []
        for i in range(3 ** 5):
            possible.append([])

        for secretWord in self.possibleWords:
            possible[compareWords(secretWord, word)].append(secretWord)

        entropy = 0
        for firstResult in range(3 ** 5):
            if len(possible[firstResult]) == 0:
                continue

            max = 0
            for guess in self.words:
                guessEntropy = self.computeSimulationEntropy(guess, possible[firstResult])
                if guessEntropy > max:
                    max = guessEntropy
            
            prob = len(possible[firstResult]) / len(self.possibleWords)
            entropy = entropy + prob * max

        return entropy


    def getBestWord(self):
        if len(self.possibleWords) == 0:
            return None
        if len(self.possibleWords) == 1:
            return self.possibleWords[0]

        score0 = 0
        score1 = 0
        for i in range(len(self.possibleWords[0])):
            score0 += self.freq[string.ascii_uppercase.index(self.possibleWords[0][i])][i]
            score1 += self.freq[string.ascii_uppercase.index(self.possibleWords[1][i])][i]

        if score0 > score1:
            return self.possibleWords[0]
        else:
            return self.possibleWords[1]

    def hash(self, word):
        p = 1
        hash = 0
        for c in word:
            hash = hash * p + int(c)
            p *= PRI

        return hash

    def isPossible(self, word):
        if hash(word) in self.possible:
            return True
        return False

    def compare(self, t):
        return -t[0], -int(t[2] * 10), t[1], -t[2]

    def chooseWord(self, layer = 1):
        if len(self.guesses) == 0:
            return FIRST
        elif len(self.guesses) == 1:
            return self.secondChoice[self.guesses[0]]
        elif len(self.guesses) == 2:
            return self.third[self.guesses[0] * 243 + self.guesses[1]]
        if len(self.possibleWords) <= 2:
            return self.getBestWord()

        entropies = []
        for word in self.words:
            result = self.computeEntropy(word)
            entropies.append([result, word, self.isPossible(word)])

        numberOfCandidates = min(5, len(self.possibleWords))
        if len(self.possibleWords) >= 1000:
            numberOfCandidates = 45
        elif len(self.possibleWords) >= 100:
            numberOfCandidates = 12

        entropies.sort(key = self.compare)
        candidates = entropies[:numberOfCandidates]

        if layer == 1:
            return candidates[0][1]

        bestResult = 0
        bestWord = None
        for word in candidates:
            simulationResult = self.simulate(word[1]) + word[0]
            if simulationResult > bestResult:
                bestResult = simulationResult
                bestWord = word[1]

        return bestWord

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
        self.guesses.append(value)

        newList = []
        for secretWord in self.possibleWords:
            if compareWords(secretWord, word) == value:
                newList.append(secretWord)
            else:
                self.possible.remove(hash(secretWord))
        self.possibleWords = newList
