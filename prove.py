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

def findLastIndex2(r, h, dimensions, threshold,textFinal):
    x = len(r)
    y = len(h)
    print(">>> x: ",x," y:",y)
    substitution = 0 # 0
    deletion = 0    # 1
    insertion = 0   # 2
    correct = 0     # 3
    textTag = []
    countCharlecter = 0
    getValue = False
    lastIndex = [0,0]
    if(textFinal):
        overTheshold = True
        getValue = True
    else:
        overTheshold = False

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
            # correct
            x = x-1
            y = y-1
            correct = correct + 1
            countCharlecter += 1

            if(countCharlecter == 1):
                textTag = []
                substitution = 0 # 0
                deletion = 0    # 1
                insertion = 0   # 2
                correct = 0     # 3
                getValue = True                
                lastIndex = [x, y]

            if(countCharlecter >=1):
                textTag.append((3, (h[y])))  

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

    # print(">>>", substitution, deletion, insertion, correct)
    textTag.reverse()
    if((lastIndex[0]<threshold or lastIndex[1]<threshold) and  not textFinal):
        lastIndex =[]
    dataReturn = {"abstract": (substitution, deletion, insertion, correct), "textTag": textTag,"lastIndex":lastIndex}
    return dataReturn

def getChunk(r, h, threshold,textFinal):
    # print("chunk : ", r, " >> ", h)
    print(">>> getChunk funtion")
    dimensions = generateMatrix(r, h)
    lastIndex = findLastIndex2(r, h, dimensions, threshold,textFinal)

    return lastIndex

def WER(r, h):
    # print("WER r\n", r, "\n h : ", h)
    print(">>> WER funtion")
    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """
    print(">>> length r :{}\n>>> length h :{}".format(len(r),len(h)))
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
    substitution = 0 # 0
    deletion = 0    # 1
    insertion = 0   # 2
    correct = 0     # 3
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

def writeHtml(provText,fileName):
    # resultDict = {"WER": result*100, "substitution": substitution,
    #  "memoryOverload": memoryOverload,
    #  "deletion": deletion, "insertion": insertion, "correct": correct,
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

        .correct {
        }
        </style>
    </head>
    <body>"""%fileName

    dictTage = {
        0: "substitution",
        1: "deletion",
        2: "insertion",
        3: "correct"
    }
    vowelsThai = ['่','้','๊','๋','็','ั','ั']

    # html += """
    # <div >Accuracy : {}</div> 
    # <div class="substitution">Substitution : {}</div> 
    # <div class="deletion">Deletion : {}</div>
    # <div class="insertion">Insertion : {}</div> 
    # <div class="correct">Correct : {}</div>
    # <div>Total : {}</div><br>  """.format(100-resultDict["WER"],resultDict["substitution"],resultDict["deletion"],resultDict["insertion"],
    # resultDict["correct"],0)
    notShow =["resultDict","chunkList","PID"]
    for item in provText:
        if(item in notShow):
            continue
        html += "<div >{} : {}</div> ".format(item.capitalize(),provText[item])
    for listTage in resultDict["textTag"]:
        if(listTage[0] != 0 and listTage[0] != 1):
            html += "<span class='{}'>{}</span>".format(
                dictTage[listTage[0]], listTage[1])
        elif(listTage[0] == 1):
            html += "<span class='{}'>{}</span>".format(
                dictTage[listTage[0]], listTage[1])
        else:
            charCorrect = listTage[1][1]
            charSub = listTage[1][0]
            if(charSub in vowelsThai):
                charSub = "&nbsp;{}&nbsp;".format(charSub)
            if(charCorrect in vowelsThai):
                charCorrect = "&nbsp;{}&nbsp;".format(charCorrect)
            html += "<span class='{0}'>{1}({2})</span>".format(
                dictTage[listTage[0]], charCorrect,charSub)
            
            



    html += """
    </body>
    </html>
    """
    for i in range(1,501,1):
        if(not os.path.isfile("output/{}[{}].html".format(fileName,i))):
            break
    with codecs.open("output/{}[{}].html".format(fileName,i), 'w', encoding="utf-8") as file:
        file.write(html)


def measureByWER(r, h, threshold, chunkSize, maxLength):
    # warring
    # for string format [:num +1] because getChunk return index(index start with 0)
    indexReference = 0
    indexHypothesis = 0
    chunkList = []
    substitution = 0
    deletion = 0
    insertion = 0
    correct = 0
    upChunkSize = 0
    isFinal = False
    memoryOverload = False
    print("\nlength r :",len(r),"\nlength h :",len(h))
    textTag = []

    while(not isFinal):
        # print("-------------------------\n")
        if(len(r[indexReference:indexReference+chunkSize+upChunkSize]) <= maxLength and
           len(h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize]) <= maxLength):
            if((indexReference+chunkSize+upChunkSize>=len(r)) and (indexHypothesis+chunkSize+upChunkSize>=len(h))):
                textFinal = True
            else:
                textFinal = False
            resultChunk = getChunk(r[indexReference:indexReference+chunkSize+upChunkSize],
                                 h[indexHypothesis:indexHypothesis+chunkSize+upChunkSize], threshold,textFinal)
            lastIndex = resultChunk['lastIndex']
        else:
            memoryOverload = True
            break
        # dataReturn = {"abstract": (
        # substitution, deletion, insertion, correct), "textTag": textTag}
        print("last index :", lastIndex)
        # not match or correct lower threshold
        if(lastIndex == []):
            # check last char in ref and hyp
            if(((indexReference+chunkSize >= len(r)-1) or (indexHypothesis+chunkSize >= len(h)-1)) and
               (len(r[indexReference:]) <= maxLength) and len(h[indexHypothesis:]) <= maxLength):
                werData = resultChunk
                indexReference += len(r[indexReference:])-1
                indexHypothesis += len(h[indexHypothesis:])-1
                chunkList.append(
                    (r[indexReference:], h[indexHypothesis:], werData["abstract"]))
                isFinal = True
            else:
                # If large jump (large upChunkSize) may to condition memoryOverload
                upChunkSize += 2000
                continue
                # print(">>> up chunk size to %s" % upChunkSize)

        # threshold ok
        else:
            upChunkSize = 0
            werData = resultChunk
            chunkList.append((r[indexReference:indexReference+lastIndex[0]+1],
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

    print("\n\n>>>", substitution, deletion, insertion, correct)
    result = float((substitution+deletion+insertion)/len(r))
    resultDict = {"memoryOverload": memoryOverload,"WER": result*100, "substitution": substitution, 
                  "deletion": deletion, "insertion": insertion, "correct": correct,
                  "chunkList": chunkList, "textTag": textTag}
    return resultDict


def testRun(r,h,rPath,hPath,chunkSize,threshold,fileName):
    # r = "เราไปทำงานที่นี่น้า"
    # h = "เรไปทงานที่นี่น้ะ"

    # threshold = 10
    # chunkSize = 500
    maxLength = 20000

    process = psutil.Process(os.getpid())
    startTime = time.time()
    resultDict = measureByWER(r, h, threshold, chunkSize, maxLength)
    endTime = time.time()
    
    memeryUse = process.memory_info().rss*0.000001
    provText = {
        "pathFileNameRef": rPath,
        "pathFileNameHyp": hPath,
        "memoryOverload": resultDict["memoryOverload"],
        "start": startTime,
        "endTime": endTime,
        "duration": endTime-startTime,
        "totalCorrect":len(r),
        "totalRaw":len(h),
        "resultDict":resultDict,
        "substitution": resultDict["substitution"],
        "deletion": resultDict["deletion"],
        "insertion": resultDict["insertion"],
        "correct": resultDict["correct"],
        "characterErrorRate": resultDict["WER"],
        "accuracy":100 - resultDict["WER"],
        "maxLength": maxLength,
        "threshold": threshold,
        "chunkSize": chunkSize,
        "PID": os.getpid(),
        "memeryUse": memeryUse,
        "chunkList": resultDict["chunkList"]
    }
    writeHtml(provText,fileName)
    return provText
    # with codecs.open("./output/output_prove.json", 'w', encoding="utf-8") as file:
    #     file.write(str(json.dumps(provText, indent=4)))


if __name__ == "__main__":
    import os
    import psutil
    import time
    import json
    import psutil
    # 0 substitution
    # 1 deletion
    # 2 insertion
    # 3 correct

    def genPathFile(directory,keyFile=None):
        files = os.listdir(directory)
        allPath =[]
        for fileName  in files:
            if(not keyFile):
                allPath.append(os.path.join(directory,fileName))
            else:
                if(keyFile in fileName):
                    allPath.append(os.path.join(directory,fileName))
        return allPath
    rDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/correct"
    hDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/raw/partii/"
    rPath = genPathFile(rDir,"NEW")
    hPath = genPathFile(hDir,"NEW")

    threshold = 100
    # size = range(2000,3000)
    size= [3000]
    print(">>> size :",size)
    
    
    for j,path in enumerate(rPath):
        for i,chunkSize in enumerate(size):
            with codecs.open(rPath[j], 'r', encoding="utf-8") as file:
                filer = file.read().lower()
                filer = filer.replace(" ","")
                filer = filer.replace("\n","")
                filer = filer.replace("\r","")
            with codecs.open(hPath[j], 'r', encoding="utf-8") as file:
                fileh = file.read().lower()
                fileh = fileh.replace(" ","")
                fileh = fileh.replace("\n","")
                fileh = fileh.replace("\r","")

                fileName = os.path.splitext(os.path.split(hPath[j])[1])[0]
            dataTest = testRun(filer,fileh,rPath[j],hPath[j],chunkSize,threshold,fileName)

        with codecs.open("./output/{}[{}].json".format(fileName,j), 'w', encoding="utf-8") as file:
            file.write(json.dumps(dataTest,indent=4,ensure_ascii=False))


    def finished():
        import winsound
        # milliseconds
        freq = 400  # Hz
        duration = 450
        for i in range(2):        
            winsound.Beep(freq, duration)
            duration -= 100
    finished()