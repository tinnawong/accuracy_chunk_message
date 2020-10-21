import os
import codecs
from WER_ import get_word_error_rate

# จาก begin เราเก็บไฟล์ไว้จากนั้นนำไฟล์มาวัดด้วย WER_ เพื่อเทียบกับแบบ prove
# pathCorrect= "output\correct"
# pathRaw = "output/raw"
# print(os.listdir(pathCorrect))
# for i,textFile in enumerate(os.listdir(pathCorrect)):
#     with codecs.open(os.path.join(pathCorrect,"output_prove%s.txt"%i),'r',encoding="utf-8") as file:
#         r = file.read()
#     with codecs.open(os.path.join(pathRaw,textFile),'r',encoding="utf-8") as file:
#         h = file.read()
#     get_word_error_rate(r,h)
#     print("\n")

# from unicategories import unicodedata
# def isMn(aChar):
#     cc = u'{}'.format(aChar)
#     try:
#         if(unicodedata.category(cc)=="Mn"):
#             return 1
#         else:
#             return 0
#     except Exception as e:
#         print(">>> Error in isMn function :",e)
#         return 0

import json
from prove import writeHtml 
with codecs.open("output/3136 fix[0].json",'r',encoding="utf-8") as file:
        r = file.read()
        result = json.loads(r)

writeHtml(result,"3136-begin2")






import codecs,os

def genPathFile(directory, keyFile=None):
        files = os.listdir(directory)
        allPath = []
        for fileName in files:
            print(fileName)
            if(not keyFile):
                if os.path.isfile(os.path.join(directory, fileName)):
                    allPath.append(os.path.join(directory, fileName))
            else:
                if(keyFile in fileName):
                    if os.path.isfile(os.path.join(directory, fileName)):
                        allPath.append(os.path.join(directory, fileName))
        return allPath

pathFile ="C:/Users\Admin\Desktop\เทียบเฉลย\ไฟล์ทดสอบเพิ่มเติม"

print(genPathFile(pathFile,""))
# for i,path in enumerate(genPathFile(pathFile,"")):
#     print("take file [{}]".format(i))
#     with codecs.open(path,"r",encoding="utf-8-sig") as ff:
#         # gg = ff.read()
#         f = ff.read().lower()
#         f = f.replace(" ", "")
#         f = f.replace("\n", "")
#         gg = f.replace("\r", "")

        
#     with codecs.open(path,"w",encoding="utf-8") as f:
#         f.write(gg)
