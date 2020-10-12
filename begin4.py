

import os,codecs
# def genPathFile(directory):
#     files = os.listdir(directory)
#     allPath =[]
#     for fileName  in files:
#         allPath.append(os.path.join(directory,fileName))
#     return allPath

# rDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/correct"
# hDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/raw/google"
# rPath = genPathFile(rDir)
# hPath = genPathFile(hDir)
# with codecs.open("./output/tt.txt", 'w', encoding="utf-8") as file:
#     text =""
#     for p in rPath:
#         text += p+"\n"
#     text += "\n\n"
#     for p in hPath:
#         text += p+"\n"
#     file.write(text)

vowel = ["่","้"]
while(1):
    v  = input("input : ")
    if(v in vowel):
        print("vowel")
    else:
        print("not vowel")