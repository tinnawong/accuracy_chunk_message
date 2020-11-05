import os
import psutil
import json,codecs

# print(os.getpid())
# process = psutil.Process(os.getpid())
# print(process.memory_info().rss) 

# อ่านไฟล์จาก output_prove.json แล้วแยกผลแต่ละ chunk เป็นไฟล์เก็บไว้เพื่อไปเทียบกับ method WER_
with codecs.open("output/3 time/25kb 3889 test[1].json",'r',encoding="utf-8") as file:
    data = file.read()
    jsonData = json.loads(data)
    
writeText =''
lengthDif = []
for i,text in enumerate(jsonData["chunkList"]):
    lengthDif.append(len(text[0])-len(text[1]))
    writeText += ">>> "+text[0]+"\n"+">>> "+text[1]+"\n"+str(text[2])+"\n\n"
    # print(">>+ ",text[0])
    # print("\n>>- ",text[1])
    # print("\n\n\n")
writeText += "length (r-h) :"+str(lengthDif)
writeText += "\nAverage length(r-h) : "+str(sum(lengthDif) / len(lengthDif) )


with codecs.open("output\output_begin.txt",'w',encoding="utf-8") as file:
    file.write(writeText)


