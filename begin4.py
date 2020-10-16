

import codecs

with codecs.open("C:/Users\Admin\Downloads\Express News ข้อความจริง.txt","r",encoding="utf-8") as f:
    text  = f.readlines()

newText = ""
for line in text:
    line = line.strip()
    if(line != ""):
        newText += line+","+str(len(line))+"\n"
    else:
        newText += "\n"
    
with codecs.open("C:/Users\Admin\Downloads\Express News ข้อความจริงพร้อมจำนวนอักขระ.txt","w",encoding="utf-8") as f:
    f.write(newText)
