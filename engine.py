from math import log2

from dataSource import DataSource
from game import compareWords

INF = 10**6
FIRST = "TAREI"

class Engine:
    class WordInfo:
        def __init__(self):
            self.entropy = 0
            self.maxCardinal = 0
            self.minCardinal = INF
            self.points = 0
            self.entropy = 0

    dataSource = DataSource()

    def __init__(self):
        self.guesses = []
        self.words = Engine.dataSource.words
        self.possibleWords = Engine.dataSource.words
        self.secondChoice = Engine.dataSource.second
        self.third = Engine.dataSource.third

    def chooseWord(self):
        if len(self.guesses) == 0:
            return FIRST
        elif len(self.guesses) == 1:
            return self.secondChoice[self.guesses[0]]
        elif len(self.guesses) == 2:
            return self.third[self.guesses[0] * 243 + self.guesses[1]]
        if len(self.possibleWords) <= 2:
            return self.possibleWords[0]
        elif len(self.possibleWords) == 0:
            return None

        bestWord = None
        max = None
        for i in range(len(self.words)):
            word = self.words[i]

            result = self.computeValue(word)
            if max == None:
                max = result
                bestWord = word
            elif max.maxCardinal > result.maxCardinal:
                max = result
                bestWord = word
            elif max.maxCardinal == result.maxCardinal and max.points < result.points:
                max = result
                bestWord = word
            elif max.maxCardinal == result.maxCardinal and max.points == result.points and max.minCardinal > result.minCardinal:
                max = result
                bestWord = word

        return bestWord

    def computeValue(self, word):
        wordInfo = self.WordInfo()

        buckets = [0] * 243
        for secretWord in self.possibleWords:
            buckets[compareWords(secretWord, word)] += 1

        wordInfo.entropy = 0
        for feedbackCode in range(3 ** 5):
            count = buckets[feedbackCode]
            if count == 0:
                continue

            wordInfo.minCardinal = min(wordInfo.minCardinal, count)
            wordInfo.points += count * self.getScore(feedbackCode)
            wordInfo.maxCardinal = max(wordInfo.maxCardinal, count)

            p = count / len(self.possibleWords)
            wordInfo.entropy = wordInfo.entropy + p * (-log2(p))

        if wordInfo.maxCardinal == 0:
            wordInfo.maxCardinal = INF

        return wordInfo

    def updateWords(self, word, value):
        self.guesses.append(value)

        newList = []
        for secretWord in self.possibleWords:
            if compareWords(secretWord, word) == value:
                newList.append(secretWord)
        self.possibleWords = newList

    def getScore(self, value):
        answer = 0
        while value > 0:
            answer += value % 3
            value //= 3
        
        return answer
