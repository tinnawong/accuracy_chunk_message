
from coppyMaxRam import genPathFile
import codecs
import json
import os
import numpy as np
import pandas as pd
import logging


def getFileName(pathFile):
    return os.path.splitext(os.path.split(pathFile)[1])[0]


def getDataFromFile(pathFile):
    with codecs.open(pathFile, 'r', encoding="utf-8") as f:
        data = f.read()
        jsonData = json.loads(data)
        # print(jsonData["accuracy"])
    return [getFileName(pathFile), jsonData]


def readThreshold(path):
    """
    read threshold in folder
    """
    databuffer = []
    for pathFile in genPathFile(path, "result.json"):
        data = getDataFromFile(pathFile)
        del data[1]["html_tag"]
        dictData = data[1]
        databuffer.append(dictData)
    databuffer.sort(key=lambda databuffer: databuffer["threshold"])
    return databuffer


def runTest2(pathTask):
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
            fileNames = ["threshold"]
            dataOFFile[fileNames[0]] = range(2, 251, 2)
            data = []

            # read data each folder
            for i, p in enumerate(os.listdir(pathTask)):
                fileNames.append(p)
                pathFile = os.path.join(pathTask, p)
                print(pathFile)
                data.append(readThreshold(pathFile))
                # if(i == 4):
                #     break

            # print(len(data))

            # check accuracy in file
            buffCheck = []

            for i, _ in enumerate(data):
                print("-------------------------------------------")
                firstCheck = True
                accuracy = 0
                listAcc = []
                for j, _ in enumerate(data[i]):
                    try:
                        # print(data[i][j]["threshold"], " ", data[i][j]["accuracy"], " ",
                        #       data[i][j]["processStatus"], " ", data[i][j]["processMessage"])
                        buffCheck.append(data[i][j]["processStatus"])
                        if(data[i][j]["processStatus"] == "success" and firstCheck):
                            data[i][j]["accuracyCheck"] = True
                            accuracy = data[i][j]["accuracy"]
                            listAcc.append(data[i][j]["accuracy"])
                            print(">>> ",accuracy)
                            firstCheck = False
                        elif data[i][j]["processStatus"] == "success" and data[i][j]["processMessage"] == "":
                            data[i][j]["accuracyCheck"] = True
                            if(accuracy != data[i][j]["accuracyCheck"] ):
                                listAcc.append(data[i][j]["accuracy"])
                        else:
                            data[i][j]["accuracyCheck"] = False

                        # if(data[i][j]["processStatus"] == "success" and data[i][j]["processMessage"] == "" and accuracy != data[i][j]["accuracy"]):
                        #     print(">>> warring accuracy :", accuracy)
                
                    except Exception as e:
                        print("Error check accuracy :", e)
                        break
                print(">>> list Acc :",listAcc)
            # buffer for visualization
            for i, _ in enumerate(data):
                buffCheck = []
                for j, d in enumerate(data[i]):

                    print(fileNames[i+1]," ",data[i][j]["threshold"], " ", data[i][j]["accuracy"], " ",
                          data[i][j]["processStatus"], " ", data[i][j]["processMessage"])
                    logging.info(fileNames[i+1]," ",data[i][j]["threshold"], " ", data[i][j]["accuracy"], " ",
                          data[i][j]["processStatus"], " ", data[i][j]["processMessage"])

                    buffCheck.append(data[i][j]["accuracyCheck"])
                dataOFFile[fileNames[i+1]] = buffCheck

            # write file
            # for k, v in dataOFFile.items():
            #     print(k, len(v), v)
            #     print("-----------------------\n")
            df1 = pd.DataFrame(dataOFFile, columns=fileNames)
            df1.to_csv("./outputReadThreshold2_1.csv", index=False)


if __name__ == "__main__":
    pathTask = "G:/ผลการทดลอง/13-1 th การทดลองthreshold"
    runTest2(pathTask)
