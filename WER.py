"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""
import numpy


def get_word_error_rate(r, h):
    print("r :", r, "\nh :", h)
    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    result = float(d[len(r)][len(h)]) / len(r) * 100
    print("First result :", result)
    x = len(r)
    y = len(h)
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0
    while True:
        if x == 0 or y == 0:
            break
        if(x == 0 and y > 0):
            # insertion
            y = y - 1
            insertion = insertion + 1
        elif(x > 0 and y == 0):
            # deletion
            x = x - 1
            deletion = deletion + 1
        elif r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            correct = correct + 1
        elif d[x][y] == d[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            substitution = substitution + 1
        elif d[x][y] == d[x - 1][y] + 1:        # deletion
            x = x - 1
            deletion = deletion + 1
        elif d[x][y] == d[x][y - 1] + 1:        # insertion
            y = y - 1
            insertion = insertion + 1
        else:
            print('\nWe got an error.')
            break
    print(">>>", substitution, deletion, insertion, correct)
    # print(float((substitution+deletion+insertion)/len(r)))
    result = float((substitution+deletion+insertion) /
                   (substitution+deletion+correct))
    resultDict = {"WER": result*100, "substitution": substitution,
                  "deletion": deletion, "insertion": insertion, "correct": correct}

    return resultDict


if __name__ == "__main__":
    import codecs
    import os
    import psutil
    import time
    import json

    r = "เราไปทำงานที่นี่น้า"
    h = "เรไปทงานที่นี่น้ะ"

    rPath = "C:/Users\Admin\Desktop\เทียบเฉลย\correct/test.txt"
    hPath = "C:/Users\Admin\Desktop\เทียบเฉลย/raw/test.txt"

    with codecs.open(rPath, 'r', encoding="utf-8") as file:
        r = file.read().replace(" ", "")
    with codecs.open(hPath, 'r', encoding="utf-8") as file:
        h = file.read().replace(" ", "")

    startTime = time.time()
    data = get_word_error_rate(r, h)
    endTime = time.time()

    process = psutil.Process(os.getpid())
    memeryUse = process.memory_info().rss
    provText = {
        "Start": startTime,
        "endTime": endTime,
        "duration": endTime-startTime,
        "substitution": data["substitution"],
        "deletion": data["deletion"],
        "insertion": data["insertion"],
        "correct": data["correct"],
        "WER": data["WER"],
        "PID": os.getpid(),
        "memeryUse": memeryUse
    }
    with codecs.open("./output/WER.json", 'w', encoding="utf-8") as file:
        file.write(str(json.dumps(provText, indent=4)))
