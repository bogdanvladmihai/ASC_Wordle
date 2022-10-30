import math

import data_source

GREY = 0
YELLOW = 1
GREEN = 2
MAX_BUCKETS = 243

word_list = []
secret_candidates = []
last_word_chosen = ""


def initEngine():
    global word_list
    word_list = data_source.getList()
    global secret_candidates
    secret_candidates = word_list


def compare(guess, secret):
    assert len(guess) == 5
    assert len(secret) == 5

    guess = guess.upper()
    secret = secret.upper()

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


def chooseWord():
    global last_word_chosen
    if len(secret_candidates) == 1:
        return secret_candidates[0]
    if len(secret_candidates) > 10000:
        last_word_chosen = 'tarie'
        return "tarie"

    max = 0
    candidate = ""
    word_with_entropy = []
    for word in word_list:
        entropy = computeEntropy(word)
        word_with_entropy.append([word, entropy])
        if max < entropy:
            max = entropy
            candidate = word

    word_with_entropy.sort(key=lambda tup: tup[1], reverse=True)

    # with open("output.txt", "w") as file:
    #     for i in word_with_entropy:
    #         print(i, file=file)

    last_word_chosen = candidate
    return candidate


def computeEntropy(word):
    count = [0] * MAX_BUCKETS
    for solution in secret_candidates:
        count[compare(word, solution)] += 1

    entropy = 0
    for bucket_size in count:
        if bucket_size == 0:
            continue
        p = bucket_size / len(secret_candidates)
        entropy += p * math.log2(1 / p)

    return entropy


def getFeedback(feedback):
    global secret_candidates
    global last_word_chosen
    new_list = []
    for word in secret_candidates:
        if feedback == compare(last_word_chosen, word):
            new_list.append(word)
    print(new_list)
    secret_candidates = new_list

# print(word_list)
