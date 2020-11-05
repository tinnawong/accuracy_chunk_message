from prove import logProcess
from multiprocessing import Process
import time
import os
def runGo():
    # file go
    os.system("cd /d E:\golang/accuracy\cmd\example/room && go run .")


if __name__ == "__main__":
    # for monitor cpu and ram of accuracy golang process
    fileName = "test"
    print(os.getpid())
    procs = []
    p2 = Process(target=logProcess, args=(fileName, "output"))
    p2.start()
    procs.append(p2)
    time.sleep(10)
    p1 = Process(target=runGo, args=())
    p1.start()
    procs.append(p1)
    for p in procs:
        p.join()
