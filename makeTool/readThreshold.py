
from coppyMaxRam import genPathFile
import codecs
import json
import os
import numpy as np
import pandas as pd
def getAccuracy(pathFile, flag=False):
    with codecs.open(pathFile, 'r', encoding="utf-8") as f:
        data = f.read()
        jsonData = json.loads(data)
        # print(jsonData["accuracy"])
    return [getFileName(pathFile), jsonData["accuracy"],jsonData["threshold"], flag]


def getFileName(pathFile):
    return os.path.splitext(os.path.split(pathFile)[1])[0]


def readThreshold(path):
    listFileCheck = []
    fileStart = genPathFile(path, "th[80]_result.json")[0]
    accuracy = getAccuracy(fileStart)[1]
    for pathFile in genPathFile(path, "result.json"):
        data = getAccuracy(pathFile)
        if(data[1] == accuracy):
            data[3] = True
            listFileCheck.append(data)
        else:
            listFileCheck.append(data)
    listFileCheck.sort(key = lambda listFileCheck: listFileCheck[2]) 

    # for f in listFileCheck:
    #     if(not f[2]):
    #         print(f)
    return listFileCheck


def runTest(pathTask):
    haveFile = False
    if os.path.isdir(pathTask):
        # check in path have sub foldler
        for p in os.listdir(pathTask):
            if os.path.isfile(os.path.join(pathTask, p)):
                haveFile = True
                print(
                    "In path have file, you should remove file befor [{}].".format(p))
                break

        if(not haveFile):
            buffData = []
            dataOFFile = {}
            fileName =["threshold"]
            dataOFFile[fileName[0]] = range(2,101,2)
            for p in os.listdir(pathTask):
                pathFile = os.path.join(pathTask, p)
                print(pathFile)
                data = readThreshold(pathFile)
                buffCheck = []
                for i,n in enumerate(range(2,101,2)):
                    try:
                        buffCheck.append(data[i][3])
                    except Exception as e:
                        buffCheck.append("")
                # output type 1
                fileName.append(p)
                dataOFFile[p] = buffCheck
                # output type 2
                buffData.extend([[p,"","",""]])
                buffData.extend(data)
                buffData.extend([["","","",""]])
            df1 = pd.DataFrame(dataOFFile, columns= fileName)
            df1.to_csv("./output_1.csv",index=False)
            df2 = pd.DataFrame(np.array(buffData),columns=['file name', 'accuracy', 'threshold','pass'])
            df2.to_csv("./output_2.csv",index=False)
            

if __name__ == "__main__":
    pathTask = "G:/ผลการทดลอง/13th การทดลองthreshold/"
    runTest(pathTask)

