

if __name__ == "__main__":
    # for check opertor between prove version and current version
    from prove import testRun,writeHtml
    import os
    import psutil
    import time
    import json
    import psutil
    import codecs
    import requests
    # 0 substitution
    # 1 deletion
    # 2 insertion
    # 3 correct

    def genPathFile(directory,keyFile=None):
        files = os.listdir(directory)
        allPath =[]
        for fileName  in files:
            if(not keyFile):
                allPath.append(os.path.join(directory,fileName))
            else:
                if(keyFile in fileName):
                    allPath.append(os.path.join(directory,fileName))
        return allPath
    rDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/correct"
    hDir = "C:/Users/tinna/Downloads/ส่งให้ทีม partii-20201011T104156Z-001/ส่งให้ทีม partii/raw/google/"
    rPath = genPathFile(rDir,"" )
    hPath = genPathFile(hDir,"")

    threshold = 100
    # size = range(2000,3000)
    size= [3000]
    print(">>> size :",size)
    
    # service test
    url = "http://127.0.0.1:5050/accuracy"

    for j,path in enumerate(rPath):
        for i,chunkSize in enumerate(size):
            with codecs.open(rPath[j], 'r', encoding="utf-8") as file:
                filer = file.read().lower()
                filer = filer.replace(" ","")
                filer = filer.replace("\n","")
                filer = filer.replace("\r","")
            with codecs.open(hPath[j], 'r', encoding="utf-8") as file:
                fileh = file.read().lower()
                fileh = fileh.replace(" ","")
                fileh = fileh.replace("\n","")
                fileh = fileh.replace("\r","")

                fileName = os.path.splitext(os.path.split(hPath[j])[1])[0]
            resultProve = testRun(filer,fileh,rPath[j],hPath[j],chunkSize,threshold,fileName,createHtml=False)
            
            # send path file
            text = dict({"pathAnswer": rPath[j],"pathSubject":hPath[j]})
            # send text
            text = dict({"textAnswer": filer,"textSubject":fileh})
            try:
                print(">>> connect glex service")
                response = requests.get(url, params=text)

                # print(">>> respones : ",json.loads(response.text))
                if(response.status_code == 200):
                    try:
                        print(">>> response glex service status ok")
                        response = json.loads(response.text)["result"]
                        math = True
                        checkList =["insertion","deletion","substitution","correction","referenceLength","hypothesisLength"]
                        for check in checkList:
                            if(resultProve[check] != response[check]):
                                print(">>> {} not match : {} != {}".format(check,resultProve[check] , response[check]))
                                math = False
                        if(not math):
                            writeHtml(resultProve,fileName)
                        else:
                            print(">>> math all chekc list")
                    except Exception as e:
                        print(e)
                        # return {"status": "failed","message":"can not format json from glex service "}
            except Exception as e:
                        print(e)
                        # return {"status": "failed","message":"can not format json from glex service "}
        with codecs.open("./output/{}[{}].json".format(fileName,j), 'w', encoding="utf-8") as file:
            file.write(json.dumps(resultProve,indent=4,ensure_ascii=False))


    def finished():
        import winsound
        # milliseconds
        freq = 400  # Hz
        duration = 450
        for i in range(2):        
            winsound.Beep(freq, duration)
            duration -= 100
    finished()