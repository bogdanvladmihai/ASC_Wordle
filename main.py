from game import Game, compareWords, toBase3
from engine import Engine
from dataSource import DataSource

import time


def startGame():
    game = Game()
    engine = Engine()

    tries = 0
    while True:
        bestWord = engine.chooseWord()
        print(f"Your best option would be {bestWord}!")

        guess, feedback = game.guess()
        tries += 1

        print(toBase3(feedback))

        if feedback == 3 ** 5 - 1:
            print(f"You have found the corret word in {tries} tries!")
            break
        
        engine.updateWords(guess, feedback)


def checkAllWords():
    file = open("solutii.txt", "w")
    index = 0
    avg = 0
    for word in DataSource.words:
        index += 1
        game = Game(word)
        engine = Engine()

        guesses = [word]
        while True:
            guess = engine.chooseWord()
            guesses.append(guess)

            if guess == game.secretWord:
                break

            value = compareWords(game.secretWord, guess)
            engine.updateWords(guess, value)

        avg += len(guesses) - 1
        if index % 100 == 0:
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
    start_time = time.time()

    for fixedHash in range(3 ** 5):
        print(fixedHash)
        engine = Engine()

        firstGuess = engine.chooseWord()
        engine.updateWords(firstGuess, fixedHash)

        secondGuess = engine.chooseWord()
        if secondGuess == None:
            secondGuess = "NOTAWORD"
        
        print(secondGuess, file = file)
        print("--- %s seconds ---" % (time.time() - start_time))

def calculateThirdStep():
    file = open("third.txt", "w")

    for first in range(3 ** 5):
        for second in range(3 ** 5):
            engine = Engine()

            firstGuess = engine.chooseWord()
            engine.updateWords(firstGuess, first)

            secondGuess = engine.chooseWord()
            thirdGuess = None
            if secondGuess != None:
                engine.updateWords(secondGuess, second)
                thirdGuess = engine.chooseWord()
            
            if thirdGuess == None:
                thirdGuess = "NOTAWORD"
            print(thirdGuess, file = file)

            print(f"{first}.{second}")
            

def getBestWord():
    engine = Engine()
    return engine.chooseWord()

# start_time = time.time()

startGame()

# print("--- %s seconds ---" % (time.time() - start_time))