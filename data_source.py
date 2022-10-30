import random

BASE = 26
words = []
words_set = set()


def word_hash(s):
    if len(s) != 5:
        return False
    answer = 0
    p = 1
    for i in range(5):
        answer += p * (ord(s[i]) - 65)
        p = p * BASE
    return answer


def isValid(s):
    if word_hash(s) in words_set:
        return True
    return False


def getRandomWord():
    pos = random.randint(0, len(words))
    return words[pos]


def getList():
    return words


def readWords():
    with open("words.txt", "r") as file:
        for line in file:
            words.append(line.rstrip("\n"))

    for word in words:
        words_set.add(word_hash(word))
    return words
