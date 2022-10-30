import data_source
import engine

GREY = 0
YELLOW = 1
GREEN = 2


def compare(guess, secret):
    assert len(guess) == 5
    assert len(secret) == 5

    code = [0] * 5
    used = [False] * 5

    for i in range(5):
        if guess[i] == secret[i]:
            code[i] = GREEN
            used[i] = True

    for i in range(5):
        if code[i] == GREEN:
            continue
        for j in range(5):
            if guess[i] == secret[j] and not used[j]:
                code[i] = YELLOW
                used[j] = True
                break

    value = 0
    for v in code:
        value = value * 3 + v

    return value


def getInput():
    while True:
        word = input("word: ")
        word = word.upper()
        if not data_source.isValid(word):
            print("Please enter valid input")
            continue
        return word


# print(compare("ABBCB", "BBEBX"))
# print(compare("ABBCB", "PBEBX"))



# data_source.readWords()
#
# is_running = True
#
# solution = data_source.getRandomWord()
# print(solution)
#
# attempts = 0
# engine.initEngine()
#
# while is_running:
#     print(engine.chooseWord())
#     userInput = getInput()
#     value = compare(userInput, solution)
#     engine.getFeedback(value)
#     attempts += 1
#
#     if value == 3 ** 5 - 1:
#         print("cuvant gasit")
#         print(f"number of attempts {attempts}")
#         is_running = False

data_source.readWords()
average = 0
for word in data_source.getList():
    is_running = True
    solution = word
    print(solution)
    engine.initEngine()

    attempts = 0
    while is_running:
        userInput = engine.chooseWord()
        userInput = userInput.upper()
        print(userInput)
        value = compare(userInput, solution)
        engine.getFeedback(value)
        attempts += 1

        if value == 3 ** 5 - 1:
            print("cuvant gasit")
            print(f"number of attempts {attempts}")
            is_running = False

    print(f"{word} - {attempts}")
    average += attempts


average /= len(data_source.getList())
print(f"average: {average}")
