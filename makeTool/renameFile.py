
if __name__ == "__main__":
    import os
    from coppyMaxRam import genPathFile
    path ="E:/python/prove-WER-method/output/11th monitor for setting (ram)/"
    for pathFile in genPathFile(path):
        os.rename(pathFile,str(pathFile).replace("'",""))