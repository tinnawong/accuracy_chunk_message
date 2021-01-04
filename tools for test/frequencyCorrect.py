    
import codecs
import clipboard

import clipboard,os
from coppyMaxRam import genPathFile
from pandas import DataFrame
import json

def getAccuracy(path):
    with codecs.open(path,'r',encoding="utf-8") as f:
        data = f.read()
        jsonData = json.loads(data)
    return jsonData["accuracy"]

if __name__ == "__main__":

    path ="G:/ผลการทดลอง/14th นับความถี่อักษรที่ถูกติดกัน"
    allPaht = genPathFile(path,"frequency.txt")
    colmList = []
    nameColm= []
    listAccuracy =[]
    for pathTask in allPaht:
        with codecs.open(pathTask, 'r', encoding="utf-8") as f:
            data = f.read().split()
            num = []
            for i in data:
                num.append(int(i))
        colmList.append(num)
        fileTask = os.path.split(pathTask)[1].split(".")[0]
        nameColm.append(fileTask)
        fileStart = fileTask.replace("frequency","result.json")
        pathFileStart = os.path.join(path,""+fileStart)
        listAccuracy.append(getAccuracy(pathFileStart))
    
    df = DataFrame (colmList).transpose()
    df.columns = nameColm
    textCop = ''
    for i in listAccuracy:
        textCop += str(i)+"\t"
    clipboard.copy(textCop)
    df.to_excel("output_frequencyCorrect.xlsx",index=False)