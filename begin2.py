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
with codecs.open("output/3136[0].json",'r',encoding="utf-8") as file:
        r = file.read()
        result = json.loads(r)

writeHtml(result,"3136-begin2")