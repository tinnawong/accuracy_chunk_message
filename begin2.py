import os
import codecs
from WER_ import get_word_error_rate

# จาก begin เราเก็บไฟล์ไว้จากนั้นนำไฟล์มาวัดด้วย WER_ เพื่อเทียบกับแบบ prve
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


text ="dfdf"

def clear(*arg):
    for i,d in enumerate(arg):
        if(isinstance(d, int)):
            d = 0
        elif(isinstance(d, str)):
            d = ""
        elif(isinstance(d, list)):
            d = []

clear(text)
print(text)