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

        guesses = [word]
        print(f"+{index}")
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
        print(f"-{index}")
        if index % 100 == 0:
            print(word)
            print(f"{index} - {(time.time() - start_time)} - avg: {avg / index}")


        for i in range(len(guesses)):
            if i > 0:
                print(", ", end = "", file = file)
            print(guesses[i], end = "", file = file)
        print(file = file)

    print(avg / len(DataSource.words))
    print(avg / len(DataSource.words), file = file)


def calculateSecondChoice():
    file = open("second.txt", "w")

    for fixedHash in range(3 ** 5):
        print(fixedHash)
        engine = Engine()

        firstGuess = engine.chooseWord()
        engine.updateWords(firstGuess, fixedHash)

        secondGuess = engine.chooseWord()
        if secondGuess == None:
            secondGuess = "NOTAWORD"
        
        print(secondGuess, file = file)

    # engine = Engine()
    # print(engine.secondChoice)
    # assert(len(engine.secondChoice) == 3 ** 5)
    # assert("X" not in engine.secondChoice)


def getBestWord():
    engine = Engine()
    word = engine.chooseWord()
    print(word)

start_time = time.time()

checkAllWords()

print("--- %s seconds ---" % (time.time() - start_time))