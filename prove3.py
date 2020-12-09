from prove import logProcess
from multiprocessing import Process
import time
import os
def runGo(pathRef,pathHyp,output,lengthText):
    # file go
    tt = """ -ldflags="-X 'gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Version=v1.5.0' -X 'main.PATHREF={}' -X 'main.PATHHYP={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Output={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Num={} " """.format(pathRef,pathHyp,output,lengthText)
    os.system("cd /d E:/golang/accuracy\cmd\example/room && go run {} .".format(tt))
def runGo2(pathRef,pathHyp,output,threshold):
    tt = """ -ldflags="-X 'gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Version=v1.5.0' -X 'main.PATHREF={}' -X 'main.PATHHYP={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Output={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.ThresholdSet={} " """.format(pathRef,pathHyp,output,threshold)
    os.system("cd /d E:/golang/accuracy\cmd\example/room && go run {} .".format(tt))


if __name__ == "__main__":
    # for monitor cpu and ram of accuracy golang process
    from prove import genPathFile
    output = "E:/python/prove-WER-method/output/"
    PATHREF = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/correct/3550_approved.txt"
    PATHHYP = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy//ไฟล์ทดสอบเพิ่มเติม/raw/3550.txt"
    getRef = genPathFile(PATHREF)
    getHyp = genPathFile(PATHHYP)
    rr = range(100,1,-2)
    for sendValue in rr:
        for i,getPath in enumerate(getRef):
            fileName = os.path.splitext(os.path.split(getHyp[i])[1])[0]
            print(os.getpid())
            procs = []
            p2 = Process(target=logProcess, args=(fileName, output,sendValue))
            p2.start()
            procs.append(p2)
            time.sleep(2)
            p1 = Process(target=runGo2, args=(getPath,getHyp[i],output,sendValue))
            p1.start()
            procs.append(p1)
            for p in procs:
                p.join()
        time.sleep(1)
