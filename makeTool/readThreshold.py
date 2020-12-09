
from coppyMaxRam import genPathFile
import codecs,json,os
def getAccuracy(pathFile,flag=False):
    with codecs.open(pathFile,'r',encoding="utf-8") as f:
        data = f.read()
        jsonData = json.loads(data)
        # print(jsonData["accuracy"])
    return [getFileName(pathFile),jsonData["accuracy"],flag]

def getFileName(pathFile):
    return os.path.splitext(os.path.split(pathFile)[1])[0]

def readThreshold(path):
    
    listFileCheck = []
    fileStart = genPathFile(path,"th[80]_result.json")[0]
    accuracy = getAccuracy(fileStart)[1]
    for pathFile in genPathFile(path,"result.json"):
        data = getAccuracy(pathFile)
        if(data[1] == accuracy):
            data[2] = True
            listFileCheck.append(data)
        else:
            listFileCheck.append(data)
    listFileCheck.sort()
    for f in listFileCheck:
        if(not f[2]):
            print(f)
if __name__ == "__main__":
    path = "E:/python/prove-WER-method/output/13th การทดลองthreshold/3543/"
    readThreshold(path)