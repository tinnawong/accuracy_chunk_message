from prove import logProcess
from multiprocessing import Process
import time
import os

def runGo(pathRef,pathHyp,output,threshold):
    tt = """ -ldflags="-X 'gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.Version=v1.5.0' -X 'main.PATHREF={}' -X 'main.PATHHYP={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.PathOutput={}' -X gitlab.spinsoft.co.th/transcription/accuracy/comparing/config.ThresholdSet={} " """.format(pathRef,pathHyp,output,threshold)
    os.system("cd /d E:/golang/accuracy\cmd\example/room && go run {} .".format(tt))


if __name__ == "__main__":
    # for monitor cpu and ram of accuracy process(golang)
    from prove import genPathFile
    output = "E:/python/prove-WER-method/output/"
    PATHREF = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/correct/3136_approved.txt"
    PATHHYP = "T:/Shared drives/งานบริษัท/เทียบเฉลย accuracy/ไฟล์ทดสอบเพิ่มเติม/raw/3136.txt"
    getRef = genPathFile(PATHREF)
    getHyp = genPathFile(PATHHYP)
    thresholdListTest = [150]
    for thresholdTest in thresholdListTest:
        for i,getPath in enumerate(getRef):
            fileName = os.path.splitext(os.path.split(getHyp[i])[1])[0]
            print(os.getpid())
            procs = []
            p2 = Process(target=logProcess, args=(fileName, output,thresholdTest))
            p2.start()
            procs.append(p2)
            time.sleep(2)
            p1 = Process(target=runGo, args=(getPath,getHyp[i],output,thresholdTest))
            p1.start()
            procs.append(p1)
            for p in procs:
                p.join()
        time.sleep(1)
