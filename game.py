import data_source

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

    print(code)

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

data_source.readWords()

is_running = True

solution = data_source.getRandomWord()
print(solution)

while is_running:
    userInput = getInput()
    value = compare(userInput, solution)

    if value == 3 ** 5 - 1:
        print("cuvant gasit")
        is_running = False



