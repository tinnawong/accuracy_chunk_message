
def normalizeText(text):
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    return text


if __name__ == "__main__":
    import codecs
    pathFile = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/correct/3391_approved - norm.txt"
    with codecs.open(pathFile,'r',encoding="utf-8") as f:
        data = f.read()
    data = normalizeText(data)
    with codecs.open(pathFile,'w',encoding="utf-8") as f:
        f.write(data)
    
    # for i in range(5000,30001,5000):
    #     print(i)
