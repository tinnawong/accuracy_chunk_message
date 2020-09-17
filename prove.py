"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""
import numpy
import codecs
# reference(r) to the hypothesis(h)


def generateMatrix(r, h):
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
    # print(dimensions)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                dimensions[i][j] = dimensions[i - 1][j - 1]
                # print(i, j, ">>>", i-1, j-1)
            else:
                # 1 2
                substitution = dimensions[i - 1][j - 1] + 1
                insertion = dimensions[i][j - 1] + 1
                deletion = dimensions[i - 1][j] + 1
                # print(i, j, "=", substitution, insertion, deletion)
                dimensions[i][j] = min(substitution, insertion, deletion)
    # print("type : ", type(dimensions[0][0]))
    # print("dimensions id (generateMatrix)", id(dimensions))
    return dimensions


def findLastIndex(r, h, dimensions, threshold):
    # print("dimensions id (findLastIndex) ", id(dimensions))
    x = len(r)
    y = len(h)

    countCharlecter = 0
    lastIndex = []
    while True:
        if x == 0 or y == 0:
            break
        # print(r[x - 1], " vs ", h[y - 1], " = ", x, y)
        if(x == 0 and y > 0):
            # insertion
            y = y - 1
            countCharlecter = 0
        elif(x > 0 and y == 0):
            # deletion
            x = x - 1
            countCharlecter = 0
        elif r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            countCharlecter += 1
            if(countCharlecter == 1):
                lastIndex = [x, y]
            if(countCharlecter >= threshold):
                return lastIndex

            # html = '%s ' % h[y] + html
        elif dimensions[x][y] == dimensions[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            countCharlecter = 0
            # html = '<span class="y">%s(%s)</span> ' % (h[y], r[x]) + html

        elif dimensions[x][y] == dimensions[x - 1][y] + 1:        # deletion
            x = x - 1
            countCharlecter = 0
            # html = '<span class="r">%s</span> ' % r[x] + html
        elif dimensions[x][y] == dimensions[x][y - 1] + 1:        # insertion
            y = y - 1
            countCharlecter = 0
            # html = '<span class="g">%s</span> ' % h[y] + html
        else:
            print('\nWe got an error.')
            break
    # Probability to return [] [num,num]
    return lastIndex


def getChunk(r, h, threshold):
    # print("chunk : ", r, " >> ", h)
    # print(">>> getChunk funtion")
    dimensions = generateMatrix(r, h)
    lastIndex = findLastIndex(r, h, dimensions, threshold)
    # try:
    #     text = "ผลของเฉลย : "+str(r[:lastIndex[0]])+"\nผลของตัวเทียบ : "+h[:lastIndex[1]]
    # except Exception as e:
    #     text = "ผลของเฉลย : "+str(r[:])+"\nผลของตัวเทียบ : "+h[:]
    #     print(e)
    # print("ผลของเฉลย : ",r[:lastIndex[0]])
    # print("ผลของตัวเทียบ : ",h[:lastIndex[1]])
    # with codecs.open("result.txt",mode='w',encoding='utf-8') as file:
    #     file.write(str(text))
    return lastIndex


def WER(r, h):
    # print("WER r\n", r, "\n h : ", h)
    # print(">>> WER funtion")
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
    # result = float(dimensions[len(r)][len(h)]) / len(r) * 100

    x = len(r)
    y = len(h)
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0
    textTag = []
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
    # print(">>>", substitution, deletion, insertion, correct)

    textTag.reverse()
    dataReturn = {"abstract": (
        substitution, deletion, insertion, correct), "textTag": textTag}
    return dataReturn


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
    with codecs.open("output/result.html", 'w', encoding="utf-8") as file:
        file.write(html)


def measureByWER(r, h, threshold, chunkSize, maxLength):
    # warring
    # for string format [:num +1] because getChunk return index(index start with 0)
    indexReference = 0
    indexHypothesis = 0
    textList = []
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0
    upChunkSize = 0
    isFinal = False
    memoryOverload = False
    # print("\nlength r :",id(r),"-",len(r)-1,"\nlength h :",id(h),"-",len(h)-1)
    textTag = []

    while(not isFinal):
        # print("-------------------------\n")
        if(len(r[indexReference:indexReference+chunkSize+upChunkSize]) <= maxLength and
           len(h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize]) <= maxLength):
            lastIndex = getChunk(r[indexReference:indexReference+chunkSize+upChunkSize],
                                 h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize], threshold)
        else:
            memoryOverload = True
            break

        # print("last index :", lastIndex)
        # not match or correct lower threshold
        if(lastIndex == []):
            # check last char in ref and hyp
            if(((indexReference+chunkSize >= len(r)-1) or (indexHypothesis+chunkSize >= len(h)-1)) and
               (len(r[indexReference:]) <= maxLength) and len(h[indexHypothesis:]) <= maxLength):
                werData = WER(r[indexReference:], h[indexHypothesis:])
                indexReference += len(r[indexReference:])-1
                indexHypothesis += len(h[indexHypothesis:])-1
                textList.append(
                    (r[indexReference:], h[indexHypothesis:], werData["abstract"]))
                isFinal = True
            else:
                # If large jump (large upChunkSize) may to condition memoryOverload
                upChunkSize += 200
                # print(">>> up chunk size to %s" % upChunkSize)

        # threshold ok
        else:
            upChunkSize = 0
            werData = WER(r[indexReference:indexReference+lastIndex[0]+1],
                          h[indexHypothesis:indexHypothesis+lastIndex[1]+1])
            textList.append((r[indexReference:indexReference+lastIndex[0]+1],
                             h[indexHypothesis:indexHypothesis+lastIndex[1]+1], werData["abstract"]))
            # sum 1 because next char
            indexReference += lastIndex[0]+1
            indexHypothesis += lastIndex[1]+1

        textTag.extend(werData['textTag'])
        substitution += werData["abstract"][0]
        deletion += werData["abstract"][1]
        insertion += werData["abstract"][2]
        correct += werData["abstract"][3]
        # print(">>> index :", indexReference, " , ", indexHypothesis)

        if((indexReference > (len(r)-1) and indexHypothesis > (len(h)-1)) or isFinal):
            break

    # print(">>> text list :", textList)
    # print(">>> text tag :", textTag)
    print("\n\n>>>", substitution, deletion, insertion, correct)
    result = float((substitution+deletion+insertion)/len(r))
    resultDict = {"WER": result*100, "substitution": substitution, "memoryOverload": memoryOverload,
                  "deletion": deletion, "insertion": insertion, "correct": correct,
                  "textList": textList, "textTag": textTag}
    writeHtml(resultDict)
    return resultDict


def testRun(chunkSize):
    r = "เราไปทำงานที่นี่น้า"
    h = "เรไปทงานที่นี่น้ะ"

    threshold = 10
    # chunkSize = 500
    maxLength = 20000

    rPath = "C:/Users\Admin\Desktop\เทียบเฉลย\correct/test2.txt"
    hPath = "C:/Users\Admin\Desktop\เทียบเฉลย/raw/test2.txt"

    with codecs.open(rPath, 'r', encoding="utf-8") as file:
        r = file.read().replace(" ", "").lower()
    with codecs.open(hPath, 'r', encoding="utf-8") as file:
        h = file.read().replace(" ", "").lower()

    startTime = time.time()
    measureByWER(r, h, threshold, chunkSize, maxLength)
    endTime = time.time()
    return endTime-startTime
    # print("WER : ", data['WER'])
    # # print("length r :",len(r)-1,"\nlength h :",len(h)-1)

    # process = psutil.Process(os.getpid())
    # memeryUse = process.memory_info().rss
    # provText = {
    #     "pathFileNameRef": rPath,
    #     "pathFileNameHyp": hPath,
    #     "memoryOverload": data["memoryOverload"],
    #     "Start": startTime,
    #     "endTime": endTime,
    #     "duration": endTime-startTime,
    #     "totalCorrect":len(r),
    #     "totalRaw":len(h),
    #     "substitution": data["substitution"],
    #     "deletion": data["deletion"],
    #     "insertion": data["insertion"],
    #     "correct": data["correct"],
    #     "WER": data["WER"],
    #     "accuracy":100 - data["WER"],
    #     "maxLength": maxLength,
    #     "threshold": threshold,
    #     "chunkSize": chunkSize,
    #     "PID": os.getpid(),
    #     "memeryUse": memeryUse,
    #     "textList": data["textList"]
    # }
    # with codecs.open("./output/output_prove.json", 'w', encoding="utf-8") as file:
    #     file.write(str(json.dumps(provText, indent=4)))


if __name__ == "__main__":
    import os
    import psutil
    import time
    import json
    # 0 substitution
    # 1 deletion
    # 2 insertion
    # 3 correct
    size = [20,30,40,50]
    timeUsed = []
    for i in size:
        usetime = testRun(i)
        timeUsed.append(usetime)
        print(">>> size {} >> {}".format(i,usetime))
        time.sleep(5)
    print(timeUsed)

    with codecs.open("./output/time use2.txt", 'w', encoding="utf-8") as file:
        file.write(str(timeUsed))