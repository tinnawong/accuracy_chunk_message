from prove import logProcess
from multiprocessing import Process
import time
import os
def runGo():
    # file go
    os.system("cd /d E:\golang/accuracy\cmd\example/room && go run .")


if __name__ == "__main__":
    # for monitor cpu and ram of accuracy golang process
    fileName = "60kb 3913"
    print(os.getpid())
    procs = []
    p2 = Process(target=logProcess, args=(fileName, "output/7th monitor system\golang prove"))
    p2.start()
    procs.append(p2)
    time.sleep(2)
    p1 = Process(target=runGo, args=())
    p1.start()
    procs.append(p1)
    for p in procs:
        p.join()
