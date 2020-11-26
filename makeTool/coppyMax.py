import codecs
import json
import os

def findMaxRam(monitor):
    buffRamUse = []
    for i, logProcess in enumerate(monitor):
        if("process" in logProcess):
            buffRamUse.append(logProcess["process"]["memory_full_info"]["rss"])
    return max(buffRamUse)

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
        files.sort()
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

    import pandas as pd

    pathUse = "../output/"
    buffMaxRam = []
    buffFileName =[]
    for fileTase in genPathFile(pathUse,"monitor.json"):
        with codecs.open(fileTase, 'r', encoding="utf-8") as f:
            data = f.read()
        jsonData = json.loads(data)
        monitor = jsonData["monitor"]
        buffMaxRam.append(findMaxRam(monitor))
        fileName = os.path.splitext(os.path.split(fileTase)[1])[0]
        buffFileName.append(fileName)
    print(buffFileName)
    print(buffMaxRam)
    df = pd.DataFrame(buffMaxRam).transpose()
    df.columns = buffFileName
    print(df.to_csv("output_coppyMax.csv",index=False,encoding="utf-8"))
    