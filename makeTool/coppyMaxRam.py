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
        if(os.path.splitext(directory)[1]):
            return [directory]
    else:
        files = os.listdir(directory)
        files = sorted(files)
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

def getLengthFile(pathFile):
    with codecs.open(pathFile,'r',encoding="utf-8") as f:
        data = f.read()
        jsonData = json.loads(data)
        print(jsonData["referenceLengthNorm"])
    return jsonData["referenceLengthNorm"],jsonData["hypothesisLengthNorm"]

if __name__ == "__main__":

    import pandas as pd

    pathUse = "E:/python/prove-WER-method/output/12 get max ram usage/3rd 3391/"
    buffMaxRam = []
    buffFileName =[]
    lengthRef = []
    langHyp = []
    for fileTask in genPathFile(pathUse,"monitor.json"):
        with codecs.open(fileTask, 'r', encoding="utf-8") as f:
            data = f.read()
        jsonData = json.loads(data)
        monitor = jsonData["monitor"]
        buffMaxRam.append(findMaxRam(monitor))
        fileName = os.path.splitext(os.path.split(fileTask)[1])[0]
        buffFileName.append(fileName)

        fileNameStart = fileName.replace("monitor","result")
        resultPath = os.path.join(os.path.dirname(fileTask),"'"+fileNameStart+".json")
        ref,hyp = getLengthFile(resultPath)
        lengthRef.append(ref)
        langHyp.append(hyp)
    
    dataWrite ={'file name':buffFileName,'max ram':buffMaxRam,"lengthRef":lengthRef,"langHyp":langHyp}
    df = pd.DataFrame(dataWrite,columns=["file name","max ram","lengthRef","langHyp"])
    df.to_excel("output_coppyMaxRam.xlsx",index=False,encoding="utf-8")
    