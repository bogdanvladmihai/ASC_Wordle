from random import randint

class DataSource:
    words = []
    second = []
    third = []

    def __init__(self):
        file = open('cuvinte_wordle.txt', 'r')
        DataSource.words = [word[:-1].upper() for word in file if len(word[:-1]) == 5]
        secFile = open("second.txt", "r")
        DataSource.second = [word[:-1].upper() for word in secFile]
        thFile = open("third.txt", "r")
        DataSource.third = [word[:-1].upper() for word in thFile]

    def getRandomWord(self):
        pos = randint(0, len(self.words))
        return DataSource.words[pos]


