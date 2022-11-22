from random import randint


class DataSource:
    words = []

    def __init__(self):
        file = open('cuvinte_wordle.txt', 'r')
        DataSource.words = [word[:-1].upper() for word in file if len(word[:-1]) == 5]

    def getRandomWord(self):
        pos = randint(0, len(self.words))
        return DataSource.words[pos]


