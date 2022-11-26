from random import randint

import string

ALPHA = 26
LEN = 5

class DataSource:
    words = []
    second = []
    third = []
    freq = []

    def __init__(self):
        file = open('cuvinte_wordle.txt', 'r')
        DataSource.words = [word[:-1].upper() for word in file if len(word[:-1]) == 5]
        secFile = open("second.txt", "r")
        DataSource.second = [word[:-1].upper() for word in secFile]
        thFile = open("third.txt", "r")
        DataSource.third = [word[:-1].upper() for word in thFile]

        for i in range(ALPHA):
            DataSource.freq.append([])
            for j in range(LEN):
                DataSource.freq[i].append(0)

        for word in DataSource.words:
            for i in range(LEN):
                DataSource.freq[string.ascii_uppercase.index(word[i])][i] += 1

    def getRandomWord(self):
        pos = randint(0, len(self.words))
        return DataSource.words[pos]


