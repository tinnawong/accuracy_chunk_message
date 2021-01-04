
if __name__ == "__main__":
    import codecs,json
    with codecs.open("../output/'3543_raw_frequency.txt",'r',encoding="utf-8") as f:
        data = f.read().strip()
        listFileName = data.split(" ")
    jj = []
    for i in listFileName:
        jj.append(int(i))

    print(max(jj))
        