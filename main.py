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
    file = open("solutions.txt", "w")
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


def getBestWord():
    engine = Engine()
    return engine.chooseWord()

start_time = time.time()

engine = Engine()
print(engine.secondChoice)
checkAllWords()

print("--- %s seconds ---" % (time.time() - start_time))