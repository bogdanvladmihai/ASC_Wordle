import os
import signal
import sys

from dataSource import DataSource
import functools

def wordIsValid(word):
    if len(word) != 5:
        return False
    if word not in DataSource.words:
        return False
    return True


def getGuess():
    guess_word = input().upper()
    while not wordIsValid(guess_word):
        guess_word = input("Your guess is invalid. Please choose another one: ").upper()
    return guess_word

def compareWords(word, guess):
    assert len(word) == 5
    assert len(guess) == 5

    code = [0] * 5
    chrset = set()
    for i in range(5):
        if word[i] == guess[i]:
            code[i] = 2
        chrset.add(word[i])

    for i in range(5):
        if code[i] == 2:
            continue
        if guess[i] in chrset:
            code[i] = 1

    value = 0
    for i in code:
        value = value * 3 + i

    return value


def getFeedback(value):
    d = {0: "Gray", 1: "Yellow", 2: "Green"}
    feedback = ""
    for i in range(5):
        feedback = d[value % 3] + ", " + feedback
        value //= 3
    return feedback[:-2]


class Game:
    dataSource = DataSource()

    def __init__(self, queue, word = None):
        self.trie = 0
        self.queue = queue
        self.secretWord = word
        sys.stdin = open(0)
        if self.secretWord is None:
            self.chooseRandomWord()

    def chooseRandomWord(self):
        self.secretWord = self.dataSource.getRandomWord()

    def guess(self):
        guess = getGuess()
        feedBack = compareWords(self.secretWord, guess)
        return guess, feedBack

    def play(self):
        tries = 0
        game_finished = False
        while not game_finished:
            guess = getGuess()
            tries += 1

            if guess == self.secretWord:
                game_finished = True
                print(f"You have guessed the word in {tries} tries")
                os.kill(os.getpid(), signal.SIGINT)
                continue

            value = compareWords(self.secretWord, guess)
            self.queue.put((guess, value))

            print(getFeedback(value))
