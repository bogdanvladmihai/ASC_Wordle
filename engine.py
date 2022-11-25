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

    def computeSimulationEntropy(self, word, secretWords):
        bucket = [0] * 3 ** 5
        for secretWord in secretWords:
            bucket[compareWords(secretWord, word)] += 1

        entropy = 0
        for count in bucket:
            if count == 0:
                continue
            p = count / len(self.possibleWords)
            entropy = entropy + p * (-log2(p))

        return entropy

    def simulate(self, guess):
        bucket = []
        for i in range(3 ** 5):
            bucket.append([])
        for secretWord in self.possibleWords:
            bucket[compareWords(secretWord, guess)].append(secretWord)

        count = 0
        for feedbackCode in range(3 ** 5):
            if len(bucket[feedbackCode]) > 0:
                count += 1

        med = 0
        for feedbackCode in range(3 ** 5):
            # print(f"Bucket id = {feedbackCode}.")
            if len(bucket[feedbackCode]) == 0:
                continue
            # Guessed the word guess and got the feedback code = feedbackCode
            # Now, I only have the words left in bucket[feedbackCode]
            # I might generate
            
            bestInfo = 0
            for word in self.words:
                bestInfo = max(bestInfo, self.computeSimulationEntropy(word, bucket[feedbackCode]))
            
            # Now I know the maximum information I can get if I chose the word guess, got the feedback code =
            # feedbackCode and gave one more guess
            prob = len(bucket[feedbackCode]) / count
            # I have to add the guess with the best information (bestInfo), knowing I can get it with probability
            # equal to prob
            # Event with profit bestInfo happends with probaility prob
            med += prob * bestInfo

        return med

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

            bestWord = None
            max = 0
            for word in l:
                entropy = self.computeEntropy(word)
                if max < entropy:
                    max = entropy
                    bestWord = word

            return bestWord
        else:
            entropies = []
            for word in self.words:
                entropy = self.computeEntropy(word)
                entropies.append([entropy, word])

            entropies.sort(reverse = True)
            numberOfCandidates = 0
            if len(self.possibleWords) > 1000:
                numberOfCandidates = 100
            elif len(self.possibleWords) >= 50:
                numberOfCandidates = 10
            else:
                numberOfCandidates = 5       

            candidates = entropies[:numberOfCandidates]
            for x in candidates:
                print(x)

            best = 0
            answer = None
            answers = []
            # id = 0
            for candidate in candidates:
                # print(f"Candidate id = {id}")
                # id += 1
                simulationResult = self.simulate(candidate[1])
                if simulationResult > best:
                    best = simulationResult
                    answer = candidate

                print(candidate[1], simulationResult)
                # answers.append([simulationResult, candidate[1]])

            answers.sort()
            outputFile = open("twosteps.txt", "w")
            for pair in answers:
                print(pair, file = outputFile)
            
            return answer

    def computeEntropy(self, word):
        buckets = [0] * 243
        for secretWord in self.possibleWords:
            buckets[compareWords(secretWord, word)] += 1

        counter = 0
        for count in buckets:
            if count > 0:
                counter += 1
            
        entropy = 0
        for count in buckets:
            if count == 0:
                continue
            p = count / counter
            entropy = entropy + p * (-log2(p))

        return entropy

    def updateWords(self, word, value):
        self.guesses += 1
        self.lastHash = value

        newList = []
        for secretWord in self.possibleWords:
            if compareWords(secretWord, word) == value:
                newList.append(secretWord)
        self.possibleWords = newList
