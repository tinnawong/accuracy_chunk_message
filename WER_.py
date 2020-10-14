"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""
import numpy


def writeHtml(resultDict):
    html = """
    <!DOCTYPE html>
    <html>
        <head>
        <meta charset='utf-8'>
        <title>Page Title</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>
            .substitution {
                color: rgb(0, 199, 27);
            }

            .deletion {
                color: crimson;
            }

            .insertion {
                color: darkblue;
            }

            .correct {
                color: rgb(0, 0, 0);
            }
        </style>
    </head>
    <body>
    """
    dictTage = {
        0: "substitution",
        1: "deletion",
        2: "insertion",
        3: "correct"
    }
    html += '<span class="substitution">substitution</span> <span class="deletion">deletion</span> <span class="insertion">insertion</span> <span class="correct">correct</span><br> '
    for listTage in resultDict["textTag"]:
        if(listTage[0] != 0 and listTage[0] != 1):
            html += "<span class='{}'>{}</span>".format(
                dictTage[listTage[0]], listTage[1])
        elif(listTage[0] == 1):
            html += "<span class='{}'>( {})</span>".format(
                dictTage[listTage[0]], listTage[1])
        else:
            html += "<span class='{0}'>{2}({1})</span>".format(
                dictTage[listTage[0]], listTage[1][0], listTage[1][1])

    html += """
    </body>
    </html>
    """
    with codecs.open("output/result_WER_.html", 'w', encoding="utf-8") as file:
        file.write(html)



def get_word_error_rate(r, h):
    print("r :", r, "\nh :", h)
    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """
    dimensions = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    dimensions = dimensions.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                dimensions[0][j] = j
            elif j == 0:
                dimensions[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                dimensions[i][j] = dimensions[i - 1][j - 1]
            else:
                substitution = dimensions[i - 1][j - 1] + 1
                insertion = dimensions[i][j - 1] + 1
                deletion = dimensions[i - 1][j] + 1
                dimensions[i][j] = min(substitution, insertion, deletion)
    result = float(dimensions[len(r)][len(h)]) / len(r) * 100

    x = len(r)
    y = len(h)
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0
    textTag =[]
    while True:
        if x == 0 and y == 0:
            break
        if(x == 0 and y > 0):
            # insertion
            y = y - 1
            insertion = insertion + 1
            textTag.append((2, (h[y])))
        elif(x > 0 and y == 0):
            # deletion
            x = x - 1
            deletion = deletion + 1
            textTag.append((1, (r[x])))
        elif(r[x-1] == h[y-1]):
            # correct
            x = x-1
            y = y-1
            correct = correct + 1
            textTag.append((3, (h[y])))
        elif dimensions[x][y] == dimensions[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            substitution = substitution + 1
            textTag.append((0, (r[x], h[y])))
        elif dimensions[x][y] == dimensions[x - 1][y] + 1:        # deletion
            x = x - 1
            deletion = deletion + 1
            textTag.append((1, (r[x])))
        elif dimensions[x][y] == dimensions[x][y - 1] + 1:        # insertion
            y = y - 1
            insertion = insertion + 1
            textTag.append((2, (h[y])))
        else:
            print('\nWe got an error.')
            break
    print(">>>", substitution, deletion, insertion, correct)
    # print(float((substitution+deletion+insertion)/len(r)))
    result = float((substitution+deletion+insertion) /
                   (substitution+deletion+correct))
    textTag.reverse()
    resultDict = {"WER": result*100, "substitution": substitution,
                  "deletion": deletion, "insertion": insertion, "correct": correct,"textTag": textTag}
    writeHtml(resultDict)
    return resultDict


if __name__ == "__main__":
    import codecs
    import os
    import psutil
    import time
    import json
    # ฟังก์ชันไฟล์นี้วัดความถูกต้องแบบทั้งไฟล์ไม่ได้ตัดเป็น chunk ไฟล์นี้ใช้สำหรับเปรียบเทียบกับแบบตัดเป็น chunk
    r = "เราไปทำงานที่นี่น้า"
    h = "เรไปทงานที่นี่น้ะ"

    rPath = "C:/Users\Admin\Desktop\เทียบเฉลย\correct/test.txt"
    hPath = "C:/Users\Admin\Desktop\เทียบเฉลย/raw/test.txt"

    with codecs.open(rPath, 'r', encoding="utf-8") as file:
        r = file.read().replace(" ", "").lower()
    with codecs.open(hPath, 'r', encoding="utf-8") as file:
        h = file.read().replace(" ", "").lower()

    startTime = time.time()
    data = get_word_error_rate(r, h)
    endTime = time.time()

    process = psutil.Process(os.getpid())
    memeryUse = process.memory_info().rss
    provText = {
        "pathFileNameRef":rPath,
        "pathFileNameHyp":hPath,
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
