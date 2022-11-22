from game import Game, compareWords
from engine import Engine
from dataSource import DataSource
import time


def startGame():
    game = Game()
    engine = Engine()
    engine.chooseWord()

    # game.play()



def checkAllWords():
    avg = 0

    file = open("solutions.txt", "w")
    index = 0
    for word in DataSource.words:
        index += 1
        game = Game(word)
        engine = Engine()

        guesses = []

        tries = 0
        while True:
            guess = engine.chooseWord()
            guesses.append(guess)
            tries += 1

            if guess == game.secretWord:
                break

            value = compareWords(game.secretWord, guess)
            engine.updateWords(guess, value)

        avg += tries
        if index % 100 == 0:
            print(f"{index} - {(time.time() - start_time)} - avg: {avg / index}")

        print(f"{word} -> {guesses}", file=file)

    print(avg / len(DataSource.words))


start_time = time.time()
checkAllWords()


print("--- %s seconds ---" % (time.time() - start_time))
