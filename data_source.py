def getWords():
    words = []
    with open("words.txt", "r") as file:
        for line in file:
            words.append(line.rstrip("\n"))

    print(words)
    return words
