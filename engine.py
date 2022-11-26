from math import log2
import string

from dataSource import DataSource
from game import compareWords

INF = 10**6
FIRST = "TAREI"
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

    def getBestWord(self):
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

    def chooseWord(self):
        if len(self.guesses) == 0:
            return FIRST
        elif len(self.guesses) == 1:
            return self.secondChoice[self.guesses[0]]
        elif len(self.guesses) == 2:
            return self.third[self.guesses[0] * 243 + self.guesses[1]]
        if len(self.possibleWords) <= 2:
            return self.getBestWord()
        elif len(self.possibleWords) == 0:
            return None

        bestWord = None
        max = None
        for word in self.words:
            result = self.computeValue(word)
            if max == None:
                max = result
                bestWord = word
            elif max < result or (max == result and not self.isPossible(bestWord) and self.isPossible(word)):
                max = result
                bestWord = word

        return bestWord

    def computeValue(self, word):
        buckets = [0] * 243
        for secretWord in self.possibleWords:
            buckets[compareWords(secretWord, word)] += 1

        entropy = 0
        for feedbackCode in range(3 ** 5):
            count = buckets[feedbackCode]
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

    def getScore(self, value):
        answer = 0
        while value > 0:
            answer += value % 3
            value //= 3
        
        return answer
