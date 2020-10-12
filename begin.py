import os
import psutil
import json,codecs
print(os.getpid())
process = psutil.Process(os.getpid())
print(process.memory_info().rss) 

print(pow(2,2))

# อ่านไฟล์จาก output_prove.json แล้วแยกผลแต่ละ chunk เป็นไฟล์เก็บไว้เพื่อไปเทียบกับ method WER_
with codecs.open("output/raw[0].json",'r',encoding="utf-8") as file:
    data = file.read()
    jsonData = json.loads(data)
writeText =''

for i,text in enumerate(jsonData["chunkList"]):
    print(">>+ ",text[0])
    print("\n>>- ",text[1])
    print("\n\n\n")
    writeText += ">>> "+text[0]+"\n"+">>> "+text[1]+"\n"+str(text[2])+"\n\n"

#     with codecs.open("output\correct\output_prove%s.txt"%i,'w+',encoding="utf-8") as file:
#         file.write(text[0])
#     with codecs.open("output/raw\output_prove%s.txt"%i,'w+',encoding="utf-8") as file:
#         file.write(text[1])

with codecs.open("output\output_prove.txt",'w',encoding="utf-8") as file:
    file.write(writeText)


