

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
