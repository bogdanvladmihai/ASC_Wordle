from math import log2

from dataSource import DataSource
from game import compareWords

FIRST = "TAREI"
LAYERONELIMIT = 5

class Engine:
    dataSource = DataSource()

    def __init__(self):
        self.guesses = 0
        self.lastHash = -1
        self.words = Engine.dataSource.words
        self.possibleWords = Engine.dataSource.words
        self.secondChoice = Engine.dataSource.second

    def findPossibleWord(self, word, feedbackCode):
        l = []
        for secret in self.possibleWords:
            if compareWords(secret, word) == feedbackCode:
                l.append(secret)
        return l

    # def simulate(self, word):
    #     for feedbackCode in range(3 ** 5):
    #         # find the list of possible word after you guess word and got the feedback feedbackCode
    #         pos = self.findPossibleWord(word, feedbackCode)
    #         # Evaluate entropy of each word in pos
    #         # Take max(entropy(pos))

    #     # Compte the entropy using this info (best word entro and bucket size)
    #     return None

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
        # if len(self.possibleWords) <= LAYERONELIMIT:
        best_word = "aaaaa"
        max = 0
        l = self.possibleWords
        if len(self.possibleWords) >= 9:
            l = self.words
        for word in l:
            entropy = self.computeEntropy(word)
            if max < entropy:
                max = entropy
                best_word = word

        return best_word
        
        # entropies = []
        # i = 0
        # for word in self.words:
        #     print(i)
        #     i += 1
        #     entropies.append([self.computeEntropy(word), word])
        # print("Calculated entropies!")

        # entropies.sort()
        # numberOfCandidates = 0
        # if len(possibleWords) > 1000:
        #     numberOfCandidates = 100
        # elif len(possibleWords) >= 50:
        #     numberOfCandidates = 15
        # else:
        #     numberOfCandidates = 5       
        # candidates = entropies[-numberOfCandidates:]

        # best = 0
        # answer = "vladu"
        # for candidate in candidates:
        #     simulationResult = self.simulate(candidate)
        #     if simulationResult > best:
        #         best = simulationResult
        #         answer = candidate

        # return answer

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
