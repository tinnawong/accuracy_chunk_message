from multiprocessing import Process
import os,time,codecs
import multiprocessing


def f1(name):
    with codecs.open("output\pid.txt",'w',encoding="utf-8") as f:
        f.write(str(os.getpid()))
    print('hello1', name)

def f2(name):
    # time.sleep(0.1)
    with codecs.open("output\pid.txt",'r',encoding="utf-8") as f:
        pid = f.read()
    print('hello2', name,pid,os.getpid())


if __name__ == '__main__':
    procs = []
    p1 = Process(target=f1, args=('bob',))
    p1.start()
    procs.append(p1)
    p2 = Process(target=f2, args=('jerry',))    
    p2.start()
    procs.append(p2)
    for p in procs:
         p.join()
