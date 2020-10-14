
import codecs


def getTextFromFile(path):
    with codecs.open(path, "r", encoding="utf-8") as f:
        return f.read().replace(" ", "").replace("\n", "").replace("\t", "")


def genPatternSearch(textInput, stepLength, stepNext=1, startIndex=0, stopIndex=0):
    stepNext = stepLength - stepNext
    pattern = []
    if(stepNext < stepLength):
        while(1):
            # print(">>>",textInput[startIndex:stopIndex+stepLength],type(textInput))
            if(len(textInput[startIndex:stopIndex+stepLength]) == stepLength or isinstance(textInput, list)):
                # print(">>>",textInput[startIndex:stopIndex+stepLength])
                pattern.append(
                    "".join(textInput[startIndex:stopIndex+stepLength]))
            if(stopIndex+stepLength > len(textInput)-1):
                # print(">>> finish")
                break
            startIndex += stepLength-stepNext
            stopIndex += stepLength-stepNext
    else:
        print("exception infinite loop")
    return pattern


def calculateStatisticWord(textRaw, patterns, thresholdStatisticWord=1):
    totalResult = {}
    lastIndexSearch = len(textRaw)
    patterns = set(patterns)
    # print(">>> uni result :",patterns)
    statisticWord = {}
    for pattern in patterns:
        startIndexSearch = 0
        while(1):
            indexWord = textRaw[startIndexSearch:lastIndexSearch].find(pattern)
            if(indexWord != -1):
                # print("\n>>> pattern :",pattern)
                # print(">>> look at :",textRaw[startIndexSearch:lastIndexSearch])
                # print(">>> result :%s"%indexWord,pattern)

                if(pattern in statisticWord):
                    indexWordRaw = indexWord + startIndexSearch
                    statisticWord[pattern][0].append(
                        [indexWordRaw, indexWord+len(pattern)-1])
                else:
                    statisticWord[pattern] = [
                        [[indexWord, indexWord+len(pattern)-1]]]

                startIndexSearch += indexWord + len(pattern)
            else:
                break
    # print(json.dumps(statisticWord,indent=4))
    statisticWordTh = {}
    for word in statisticWord:
        if(len(statisticWord[word][0]) >= thresholdStatisticWord):
            statisticWordTh[word] = statisticWord[word]

    with codecs.open("./output/statisticWord.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(statisticWord, indent=4, ensure_ascii=False))

    with codecs.open("./output/statisticWordTh.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(statisticWordTh, indent=4, ensure_ascii=False))
    return statisticWordTh


if __name__ == "__main__":

    from glexSegment import Glex
    import re
    import json
    glex = Glex()

    pathFile = "C:/Users\Admin\Desktop\เทียบเฉลย\สำหรับทดสอบ\correct test/50kb 3922_310863_หลักการเขียนโปรแกรม (ปี1) test.txt"
    # pathFile = "./rTest.txt"
    textRaw = getTextFromFile(pathFile)
    with codecs.open("./output/fileTest.txt", "w", encoding="utf-8") as f:
        f.write(textRaw)
    # segment 
    textSegment = glex.glexSegment(textRaw)["results"]
    stepLength = 4
    stepNext = 1
    # startIndex =0
    # stopIndex = 0
    thresholdStatisticWord = 2
    patterns = genPatternSearch(textSegment, stepLength, stepNext)
    calculateStatisticWord(textRaw, patterns, thresholdStatisticWord)
