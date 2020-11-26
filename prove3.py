from prove import logProcess
from multiprocessing import Process
import time
import os
def runGo(pathRef,pathHyp,output):
    # file go
    tt = """ -ldflags="-X 'gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Version=v100' -X 'main.PATHREF={}' -X 'main.PATHHYP={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Output={}' " """.format(pathRef,pathHyp,output)
    os.system("cd /d E:\golang/accuracy\cmd\example/room && go run {} .".format(tt))


if __name__ == "__main__":
    # for monitor cpu and ram of accuracy golang process
    from prove import genPathFile
    output = "E:/python/prove-WER-method/output/"
    PATHREF = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/correct/"
    PATHHYP = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/raw/"
    getRef = genPathFile(PATHREF)
    getHyp = genPathFile(PATHHYP)
    
    for i,getPath in enumerate(getRef):
        fileName = os.path.splitext(os.path.split(getHyp[i])[1])[0]
        print(os.getpid())
        procs = []
        p2 = Process(target=logProcess, args=(fileName, output))
        p2.start()
        procs.append(p2)
        time.sleep(2)
        p1 = Process(target=runGo, args=(getPath,getHyp[i],output))
        p1.start()
        procs.append(p1)
        for p in procs:
            p.join()
