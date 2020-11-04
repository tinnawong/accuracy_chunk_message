import numpy
import codecs
import re
import os
import psutil
import time
import json
from unicategories import unicodedata
from multiprocessing import Process
import platform
import git
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


def findLastIndex2(r, h, dimensions, threshold, textFinal):
    x = len(r)
    y = len(h)
    print(">>> x: ", x, " y:", y)
    substitution = 0  # 0
    deletion = 0    # 1
    insertion = 0   # 2
    correction = 0     # 3
    textTag = []
    countCharlecter = 0
    lastIndex = [0, 0]

    if(textFinal):
        overTheshold = True
        getValue = True
        lastIndex = [x-1, y-1]
    else:
        overTheshold = False
        getValue = False

    while True:
        if x == 0 and y == 0:
            break
        if(x == 0 and y > 0):
            # insertion
            y = y - 1
            insertion = insertion + 1
            if(not overTheshold):
                countCharlecter = 0
            if(getValue):
                textTag.append((2, (h[y])))
        elif(x > 0 and y == 0):
            # deletion
            x = x - 1
            deletion = deletion + 1
            if(not overTheshold):
                countCharlecter = 0
            if(getValue):
                textTag.append((1, (r[x])))
        elif(r[x-1] == h[y-1]):
            # correction
            x = x-1
            y = y-1

            countCharlecter += 1
            if(countCharlecter == 1 and not textFinal):
                textTag = []
                substitution = 0  # 0
                deletion = 0    # 1
                insertion = 0   # 2
                correction = 0     # 3
                getValue = True
                lastIndex = [x, y]
            textTag.append((3, (h[y])))

            correction = correction + 1

            if(countCharlecter >= threshold):
                overTheshold = True

        elif dimensions[x][y] == dimensions[x - 1][y - 1] + 1:
            # substitution
            x = x - 1
            y = y - 1
            substitution = substitution + 1
            if(not overTheshold):
                countCharlecter = 0
            if(getValue):
                textTag.append((0, (r[x], h[y])))
        elif dimensions[x][y] == dimensions[x - 1][y] + 1:
            # deletion
            x = x - 1
            deletion = deletion + 1
            if(not overTheshold):
                countCharlecter = 0
            if(getValue):
                textTag.append((1, (r[x])))
        elif dimensions[x][y] == dimensions[x][y - 1] + 1:
            # insertion
            y = y - 1
            insertion = insertion + 1
            if(not overTheshold):
                countCharlecter = 0
            if(getValue):
                textTag.append((2, (h[y])))
        else:
            print('\nWe got an error.')
            break

    # print(">>>", substitution, deletion, insertion, correction)
    textTag.reverse()
    if((lastIndex[0] < threshold or lastIndex[1] < threshold) and not textFinal):
        lastIndex = [0, 0]
    dataReturn = {"abstract": (substitution, deletion, insertion,
                               correction), "textTag": textTag, "lastIndex": lastIndex}
    return dataReturn


def getChunk(r, h, threshold, textFinal):
    print(">>> getChunk funtion is final:", textFinal)
    dimensions = generateMatrix(r, h)
    lastIndex = findLastIndex2(r, h, dimensions, threshold, textFinal)

    return lastIndex


def isMn(aChar):
    cc = u'{}'.format(aChar)
    charManage = ["ำ"]
    try:
        if(unicodedata.category(cc) == "Mn" or aChar in charManage):
            return 1
        else:
            return 0
    except Exception as e:
        print(">>> Error in isMn function :", e)
        return 0


def writeHtml(provText, fileName, pathOutput):

    resultDict = provText['resultDict']
    html = """
    <!DOCTYPE html>
    <html>
        <head>
        <meta charset='utf-8'>
        <title>%s</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>
        .substitution {
            background-color: #ffa50099;
        }

        .deletion {
            background-color: #ff00004d;
        }

        .insertion {
            background-color: #0080004d;
        }

        .correction {
        }
        </style>
    </head>
    <body>""" % fileName

    dictTage = {
        0: "substitution",
        1: "deletion",
        2: "insertion",
        3: "correction"
    }
    notShow = ["resultDict", "chunkList", "PID"]
    for item in provText:
        if(item in notShow):
            continue
        html += "<div >{} : {}</div> ".format(
            item.capitalize(), provText[item])

    substitutionBuffer = []
    for i, listTage in enumerate(resultDict["textTag"]):
        # 0 substitution
        # 1 deletion
        # 2 insertion
        # 3 correction
        if(listTage[0] != 0):
            # for check befor if is subtitution do this condition
            if(substitutionBuffer != []):
                charCorrect = ''.join([str(elem[1])
                                       for elem in substitutionBuffer])
                charSub = ''.join([str(elem[0])
                                   for elem in substitutionBuffer])
                if(isMn(charCorrect[0])):
                    charCorrect = "-"+charCorrect
                if(isMn(charSub[0])):
                    charSub = "-"+charSub

                html += "<span class='{0}'>{1}({2})</span>".format(
                    dictTage[0], charCorrect, charSub)
                substitutionBuffer = []

            if(i >= 1):
                # (เ)-้ or ดิ -> -ิ wrong
                if((resultDict["textTag"][i-1][0] == 0 and isMn(listTage[1])) or (isMn(listTage[1]) and
                                                                                  (resultDict["textTag"][i-1][0] != resultDict["textTag"][i-1][0]))):
                    html += "<span class='{}'>-{}</span>".format(
                        dictTage[listTage[0]], listTage[1])

                elif (isMn(listTage[1]) and re.findall("[ก-ฮ]", listTage[1])):
                    html += "<span class='{}'>-{}</span>".format(
                        dictTage[listTage[0]], listTage[1])
                else:
                    html += "<span class='{}'>{}</span>".format(
                        dictTage[listTage[0]], listTage[1])
            else:
                html += "<span class='{}'>{}</span>".format(
                    dictTage[listTage[0]], listTage[1])

        else:
            substitutionBuffer.append((listTage[1][0], listTage[1][1]))

    html += """
    </body>
    </html>
    """
    for i in range(1, 501, 1):
        if(not os.path.isfile("output/{}[{}].html".format(fileName, i))):
            break
    with codecs.open(os.path.join(pathOutput, "{}[{}].html".format(fileName, i)), 'w', encoding="utf-8") as file:
        file.write(html)


def measureByWER(r, h, threshold, chunkSize, maxLength):
    # warring
    # for string format [:num +1] because getChunk return index(index start with 0)
    indexReference = 0
    indexHypothesis = 0
    hypothesisLength = len(h)
    chunkList = []
    substitution = 0
    deletion = 0
    insertion = 0
    correction = 0
    upChunkSize = 0
    textFinal = False
    memoryOverload = False
    print("\nlength r :", len(r), "\nlength h :", len(h))
    textTag = []
    progress = 0
    while(not textFinal):
        # print("-------------------------\n")
        # get chunk with operator
        progress = indexHypothesis*100/hypothesisLength
        print(">>> progress : {} %".format(progress))
        if(len(r[indexReference:indexReference+chunkSize+upChunkSize]) <= maxLength and
           len(h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize]) <= maxLength):
            if((indexReference+chunkSize+upChunkSize >= len(r)) and (indexHypothesis+chunkSize+upChunkSize >= len(h))):
                textFinal = True
            else:
                textFinal = False
            resultChunk = getChunk(r[indexReference:indexReference+chunkSize+upChunkSize],
                                   h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize], threshold, textFinal)
            lastIndex = resultChunk['lastIndex']
        else:
            memoryOverload = True
            break

        print("last index :", lastIndex)

        # not match or correct lowe than threshold
        if(lastIndex == [0, 0] and not textFinal):
            # If large jump (large upChunkSize) may to condition memoryOverload
            upChunkSize += 2000
            print(">>> up chunk size to %s" % upChunkSize)
            continue

        # over threshold
        else:
            upChunkSize = 0
            chunkList.append((r[indexReference:indexReference+lastIndex[0]+1],
                              h[indexHypothesis:indexHypothesis+lastIndex[1]+1], resultChunk["abstract"]))
            # sum 1 because next char
            indexReference += lastIndex[0]+1
            indexHypothesis += lastIndex[1]+1

        textTag.extend(resultChunk['textTag'])
        substitution += resultChunk["abstract"][0]
        deletion += resultChunk["abstract"][1]
        insertion += resultChunk["abstract"][2]
        correction += resultChunk["abstract"][3]

    print("\n\n>>>", substitution, deletion, insertion, correction)
    result = float((substitution+deletion+insertion)/len(r))
    resultDict = {"memoryOverload": memoryOverload, "WER": result*100, "substitution": substitution,
                  "deletion": deletion, "insertion": insertion, "correction": correction,
                  "chunkList": chunkList, "textTag": textTag}
    return resultDict


def testRun(r, h, rPath, hPath, chunkSize, threshold, fileName, createHtml=True):
    maxLength = 20000
    print(">>> PID :", os.getpid())
    with codecs.open("output\pid.txt", 'w', encoding="utf-8") as f:
        f.write(str(os.getpid()))

    process = psutil.Process(os.getpid())
    startTime = time.time()
    resultDict = measureByWER(r, h, threshold, chunkSize, maxLength)
    endTime = time.time()

    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    provText = {
        "pathFileNameRef": rPath,
        "pathFileNameHyp": hPath,
        "memoryOverload": resultDict["memoryOverload"],
        "start": startTime,
        "endTime": endTime,
        "duration": endTime-startTime,
        "referenceLength": len(r),
        "hypothesisLength": len(h),
        "resultDict": resultDict,
        "substitution": resultDict["substitution"],
        "deletion": resultDict["deletion"],
        "insertion": resultDict["insertion"],
        "correction": resultDict["correction"],
        "characterErrorRate": resultDict["WER"],
        "accuracy": 100 - resultDict["WER"],
        "maxLength": maxLength,
        "threshold": threshold,
        "chunkSize": chunkSize,
        # "processor": {"platform":"",
        #               "RAM":"",
        #               "":"",
        #               "":"",
        #               "":"",
        #               "":""},
        "commitCode": sha
    }
    if(provText["deletion"]+provText["substitution"]+provText["correction"] != provText["referenceLength"]):
        print("\n\nError deletion + substitution + correction != referenceLength\n")
    if(provText["insertion"]+provText["substitution"]+provText["correction"] != provText["hypothesisLength"]):
        print("\n\nError insertion + substitution + correction != hypothesisLength\n")

    if(1):
        writeHtml(provText, fileName, "output/7th monitor system/")

    with codecs.open("./output/7th monitor system/{}.json".format(fileName), 'w', encoding="utf-8") as file:
        file.write(json.dumps(provText, indent=4, ensure_ascii=False))

    return provText


def normalizeText(text):
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    return text


def logProcess(fileName, pathOutput):
    log = {}
    intervalCheck = 1
    pidBegin = False

    log["platformTest"] = platform.platform()
    log["architecture"] = platform.architecture()
    log["psutil_virtual_memory"] = psutil.virtual_memory()._asdict()
    log["psutil_swap_memory"] = psutil.swap_memory()._asdict()
    log["monitor"] = []

    
    while(1):
        try:
            if(not pidBegin):
                with codecs.open("output\pid.txt", 'r', encoding="utf-8") as f:
                    pid = int(f.read().strip())
            logTime = {}
            logTime["timestamp"] = time.time()
            if(pid not in psutil.pids()):
                if(pidBegin):
                    for i in range(10):
                        print(">>> log CPU and RAM")
                        logTime["psutil_cpu_percent"] = psutil.cpu_percent(interval=intervalCheck)
                        logTime["psutil_virtual_memory"] = psutil.virtual_memory()._asdict()
                        log["monitor"].append(logTime)
                    break
                print(">>> log CPU and RAM befor start process")
                logTime["psutil_cpu_percent"] = psutil.cpu_percent(interval=intervalCheck)
                logTime["psutil_virtual_memory"] = psutil.virtual_memory()._asdict()
            else:
                # print(">>> log cpu work and ram work")
                p = psutil.Process(pid)
                pidBegin = True
                logTime["psutil_cpu_percent"] = psutil.cpu_percent()
                logTime["psutil_virtual_memory"] = psutil.virtual_memory()._asdict()
                # print(">>> ",psutil.cpu_percent(interval=0.5))
                subTimeProcess = {}
                with p.oneshot():
                    subTimeProcess["ppid"] = time.time()
                    subTimeProcess["ppid"] = p.ppid()
                    subTimeProcess["pid"] = p.pid
                    subTimeProcess["memory_percent"] = p.memory_percent()
                    subTimeProcess["cpu_percent"] = p.cpu_percent(interval=intervalCheck)/psutil.cpu_count()
                    subTimeProcess["memory_full_info"] = p.memory_full_info()._asdict()
                    logTime["process"] = subTimeProcess
                    print(">>> ",logTime["psutil_cpu_percent"],"/",subTimeProcess["cpu_percent"])
                    del subTimeProcess
            log["monitor"].append(logTime)
        except Exception as e:
            print(e, "in function logProcess")
    with codecs.open(os.path.join(pathOutput, "{}_monitor.json".format(fileName)), "w", encoding="utf-8") as f:
        f.write(json.dumps(log, indent=4, ensure_ascii=False))
    return log


def genPathFile(directory, keyFile=None):
    
    if(os.path.isfile(directory) ):
        # print(os.path.splitext(directory)[1])
        fileSupport = [".txt"]
        if(os.path.splitext(directory)[1] in fileSupport):
            return [directory]
        else:
            print(">>> file not support")
            return []
    else:
        files = os.listdir(directory)
        allPath = []
        for fileName in files:
            newPath = os.path.join(directory, fileName)
            if(os.path.isfile(newPath)):
                if(not keyFile):
                    allPath.append(newPath)
                else:
                    if(keyFile in fileName):
                        allPath.append(newPath)
        return allPath


if __name__ == "__main__":

    # 0 substitution
    # 1 deletion
    # 2 insertion
    # 3 correction

    rDir = "T:\Shared drives\งานบริษัท/เทียบเฉลย accuracy\ไฟล์ทดสอบเพิ่มเติม/correct/"
    hDir = "T:\Shared drives\งานบริษัท/เทียบเฉลย accuracy\ไฟล์ทดสอบเพิ่มเติม/raw/"
    rPath = genPathFile(rDir, "3391")
    hPath = genPathFile(hDir, "3391")

    threshold = 100
    # size = range(2000,3000)
    size = [5000]
    print(">>> size :", size)

    for j, path in enumerate(rPath):
        for i, chunkSize in enumerate(size):
            with codecs.open(rPath[j], 'r', encoding="utf-8") as file:
                filer = file.read()
                filer = normalizeText(filer)

            with codecs.open(hPath[j], 'r', encoding="utf-8") as file:
                fileh = file.read()
                fileh = normalizeText(fileh)
                fileName = os.path.splitext(os.path.split(hPath[j])[1])[0]

            print(">>> task file :", fileName, " && ",
                  os.path.splitext(os.path.split(rPath[j])[1])[0])
            # dataTest = testRun(filer, fileh, rPath[j], hPath[j], chunkSize, threshold, fileName)

            procs = []

            p2 = Process(target=logProcess, args=(fileName, "output/"))
            p2.start()
            procs.append(p2)
            time.sleep(10)
            p1 = Process(target=testRun, args=(
                filer, fileh, rPath[j], hPath[j], chunkSize, threshold, fileName))
            p1.start()
            procs.append(p1)
            for p in procs:
                p.join()

        # with codecs.open("./output/{}[{}].json".format(fileName, j), 'w', encoding="utf-8") as file:
        #     file.write(json.dumps(dataTest, indent=4, ensure_ascii=False))

    def finished():
        import winsound
        # milliseconds
        freq = 400  # Hz
        duration = 450
        for i in range(2):
            winsound.Beep(freq, duration)
            duration -= 100
    finished()
