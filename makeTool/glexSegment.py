import requests
import os
import json
import codecs


class Glex():

    def __init__(self):
        self.typeWord = {0: "UNKNOWN", 1: "KNOWN", 2: "AMBIGUOUS", 3: "ENGLISH",
                         4: "DIGIT", 5: "SPECIAL", 6: "GROUP"}
        self.hostingGlex = str(os.environ.get("HOSTING_GLEX_SEGMENT"))


    def connectGlexService(self,text,useDict=""):

        # send text to glex service
        # url = self.hostingGlex
        url = "http://127.0.0.1:8080/glexSegment"

        # text = {"text": "เป็นการจัดกลุ่ม routes ของ request ว่า request ไหนต้องมีการ "}
        text = dict({"text": text,"useDict":useDict})

        # get respone and create html file
        try:
            # print(">>> connect glex service")
            response = requests.get(url, params=text)
            # print(">>> respones : ",json.loads(response.text))
            if(response.status_code == 200):
                try:
                    # print(">>> response glex service status ok")
                    response = json.loads(response.text)
                    # print("-->>>",response)
                    if(len(response['results']) == len(response['typeLists']) and response['status'] =="ok"):            
                        try:
                            return {"status": "ok","results":response['results'],"dictName":response['dictName']}

                        except Exception as e:
                            return {"status": "failed","message":"can not create html file"}                   
            
                except Exception as e:
                    # print(e)
                    return {"status": "failed","message":"can not format json from glex service "}
            else:
                return {"status": "failed","message":"can't connect glex service(status code :{})".format(response.status_code)} 
        except Exception as e:
            # print(e)
            return {"status": "failed","message":"can't connect glex service"} 

    def glexSegment(self,text,useDict=""):
        return self.connectGlexService(text,useDict)

if __name__ == "__main__":
    # from glex import glexSeg
    # glexSeg(self, text,fileName):

    pass
