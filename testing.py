
def compare1(word, guess):
    assert len(guess) == 5
    assert len(word) == 5

    code = [0] * 5
    used = [False] * 5

    for i in range(5):
        if guess[i] == word[i]:
            code[i] = 2
            used[i] = True

    for i in range(5):
        if code[i] == 2:
            continue
        for j in range(5):
            if guess[i] == word[j] and not used[j]:
                code[i] = 1
                used[j] = True
                break

    value = 0
    for v in code:
        value = value * 3 + v

    return value


def compare2(word, guess):
    assert len(word) == 5
    assert len(guess) == 5

    code = [0] * 5
    used = [False] * 5
    for i in range(5):
        if word[i] == guess[i]:
            code[i] = 2
            used[i] = True

    for i in range(5):
        if code[i] != 0:
            continue
        for j in range(5):
            if code[j] == 2:
                continue
            if guess[i] == word[j] and not used[j]:
                code[i] = 1
                used[j] = True
                break

    value = 0
    for i in code:
        value = value * 3 + i

    return value


from dataSource import DataSource
from game import toBase3

dataSource = DataSource()

while True:

    word = dataSource.getRandomWord()
    guess = dataSource.getRandomWord()
    if compare1(word, guess) != compare2(word, guess):
        print (f"{word} {guess} {toBase3(compare1(word, guess))}, {toBase3(compare2(word, guess))}")
        break