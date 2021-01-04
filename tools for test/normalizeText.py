
def normalizeText(text):
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    return text


if __name__ == "__main__":
    import codecs
    from coppyMaxRam import genPathFile
    pathFile = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพื่อใช้ในการตั้งค่า/raw/"
    
    for ff in genPathFile(pathFile):
            with codecs.open(ff,'r',encoding="utf-8-sig") as f:
                data = f.read()
            data = normalizeText(data)
            with codecs.open(ff,'w',encoding="utf-8") as f:
                f.write(data)
    # for i in range(5000,30001,5000):
    #     print(i)
