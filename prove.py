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
    return lastIndex


def getChunk(r, h, threshold):
    print("chunk : ", r, " >> ", h)
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
    print("WER :", r, " <<>> ", h)
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
    while True:
        if x == 0 or y == 0:
            break
        if(x == 0 and y > 0):
            # insertion
            y = y - 1
            insertion = insertion +1
        elif(x > 0 and y == 0):
            # deletion
            x = x - 1
            deletion = deletion + 1

        elif(r[x-1] == h[y-1]):
            # correct
            x = x-1
            y = y-1
            correct = correct + 1
        elif dimensions[x][y] == dimensions[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            substitution = substitution + 1
        elif dimensions[x][y] == dimensions[x - 1][y] + 1:        # deletion
            x = x - 1
            deletion = deletion + 1
        elif dimensions[x][y] == dimensions[x][y - 1] + 1:        # insertion
            y = y - 1
            insertion = insertion +1
        else:
            print('\nWe got an error.')
            break
    print(">>>", substitution, deletion, insertion, correct)
    return (substitution, deletion, insertion, correct)


def measureByWER(r, h, threshold, chunkSize):
    indexReference = 0
    indexHypothesis = 0
    textList = []
    isFinal = False
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0

    # print("\nlength r :",id(r),"-",len(r)-1,"\nlength h :",id(h),"-",len(h)-1)

    while(not isFinal):
        print("-------------------------\n")
        lastIndex = getChunk(r[indexReference:indexReference+chunkSize],
                             h[indexHypothesis:chunkSize+indexHypothesis], threshold)
        # for string format [:num+1] because getChunk return index(index start with 0)

        print("last index :", lastIndex)
        # not match or lower threshold
        if(lastIndex == []):
            data = WER(r[indexReference:], h[indexHypothesis:])
            indexReference += len(r[indexReference:])-1
            indexHypothesis += len(h[indexHypothesis:])-1
            textList.append((r[indexReference:], h[indexHypothesis:]))
            isFinal = True
            # return 0
        # chunk is last sentence
        elif(lastIndex[0] == 0 and lastIndex[1] == 0):
            if((indexReference+chunkSize >= len(r)-1) or (indexHypothesis+chunkSize >= len(h)-1)):
                data = WER(r[indexReference:], h[indexHypothesis:])
                indexReference += len(r[indexReference:])-1
                indexHypothesis += len(h[indexHypothesis:])-1
                textList.append((r[indexReference:], h[indexHypothesis:]))
                isFinal = True
        # threshold ok
        else:
            data = WER(r[indexReference:indexReference+lastIndex[0]+1],
                       h[indexHypothesis:indexHypothesis+lastIndex[1]+1])
            textList.append((r[indexReference:indexReference+lastIndex[0]+1],
                             h[indexHypothesis:indexHypothesis+lastIndex[1]+1]))
            # sum 1 because next char
            indexReference += lastIndex[0]+1
            indexHypothesis += lastIndex[1]+1
        substitution += data[0]
        deletion += data[1]
        insertion += data[2]
        correct += data[3]
        print(">>> index :", indexReference, " , ", indexHypothesis)

        if((indexReference > (len(r)-1) and indexHypothesis > (len(h)-1)) or isFinal):
            # return textList,indexReference,indexHypothesis
            break
    print(textList)
    print("\n\n>>>", substitution, deletion, insertion, correct)
    result = float((substitution+deletion+insertion)/len(r))
    resultDict = {"WER": result*100, "substitution": substitution,
                  "deletion": deletion, "insertion": insertion, "correct": correct}
    return resultDict


if __name__ == "__main__":
    import os
    import psutil
    import time
    import json
    # print("PID : ",os.getpid())
    # time.sleep(2)

    r = "เราไปทำงานที่นี่น้า"
    h = "เรไปทงานที่นี่น้ะ"

    threshold = 10
    chunkSize = 1000
    rPath = "C:/Users\Admin\Desktop\เทียบเฉลย\correct/test.txt"
    hPath = "C:/Users\Admin\Desktop\เทียบเฉลย/raw/test.txt"

    with codecs.open(rPath,'r',encoding="utf-8") as file:
        r = file.read().replace(" ","")
    with codecs.open(hPath,'r',encoding="utf-8") as file:
        h = file.read().replace(" ","")

    startTime = time.time()
    data = measureByWER(r, h, threshold, chunkSize)
    endTime = time.time()

    print("WER : ", data['WER'])
    # print("length r :",len(r)-1,"\nlength h :",len(h)-1)

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
        "threshold": threshold,
        "chunkSize": chunkSize,
        "PID": os.getpid(),
        "memeryUse": memeryUse
    }
    with codecs.open("./output/output_prove.json", 'w', encoding="utf-8") as file:
        file.write(str(json.dumps(provText, indent=4)))
