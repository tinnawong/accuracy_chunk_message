import codecs,json
import matplotlib.pyplot as plt
import os
import clipboard

def plotSystem(monitor):

    xInProcess = []
    xOutPrcessAfter = []
    xOutPrcessBefor = []

    yCPUUsageIn =[]
    yMemoryUsageIn=[]

    yCPUUsageOutBefor=[]
    yMemoryUsageOutBefor=[]
    yCPUUsageOutAfter=[]
    yMemoryUsageOutAfter=[]
    checkPoint = False
    for i,element in enumerate(monitor):
        if(1):
            checkPoint = True
            yCPUUsageIn.append(element["psutil_cpu_percent"])
            yMemoryUsageIn.append(element["psutil_virtual_memory"]["percent"])
            xInProcess.append(i)
        # else:
        #     if(not checkPoint):
        #         yCPUUsageOutBefor.append(element["psutil_cpu_percent"])
        #         yMemoryUsageOutBefor.append(element["psutil_virtual_memory"]["percent"])
        #         xOutPrcessBefor.append(i)
        #     else:
        #         yCPUUsageOutAfter.append(element["psutil_cpu_percent"])
        #         yMemoryUsageOutAfter.append(element["psutil_virtual_memory"]["percent"])
        #         xOutPrcessAfter.append(i)

    plt.xlabel('time(s)')
    plt.ylabel('percent(%)')
    plt.plot(xInProcess,yCPUUsageIn)
    plt.plot(xInProcess,yMemoryUsageIn)

    plt.plot(xOutPrcessBefor,yCPUUsageOutBefor) 
    plt.plot(xOutPrcessAfter,yMemoryUsageOutAfter) 


    ax = plt.gca()
    ax.set_title(u'Monitor CPU & RAM',fontname='Tahoma',fontsize=13)
    ax.legend([u'CPU',u'Memory'])
    plt.suptitle('System')
    plt.show()

def plotProcess(monitor):
    yMemoryUsage = []
    yCPUUsage = []
    checkPoint = False
    xUsage =[]
    timeBefor = 0
    for i,logProcess in enumerate(monitor):
        if("process" in logProcess):
            if(not checkPoint):
                startTime = i
                checkPoint = True
            # print(logProcess["process"]["cpu_percent"])
            # if(timeBefor == 0):
            #     print(0)
            #     timeBefor = logProcess["timestamp"]
            # else:
            #     print(logProcess["timestamp"]-timeBefor)
            #     timeBefor = logProcess["timestamp"]

            yMemoryUsage.append(logProcess["process"]["memory_percent"])
            yCPUUsage.append(logProcess["process"]["cpu_percent"])
            xUsage.append(i)

    if(len(xUsage) == len(yCPUUsage) and len(xUsage) == len(yMemoryUsage)):
        text = ""
        for i,value in enumerate(xUsage):
            print(value,"\t",yCPUUsage[i],"\t",yMemoryUsage[i])
            text += str(yCPUUsage[i])+"\t"+str(yMemoryUsage[i])+"\n"
        clipboard.copy(text)

    plt.xlabel('time(s)')   #แกน x พร้อมตั้งชื่อในวงเล็บ
    plt.ylabel('percent(%)')   #แกน y พร้อมตั้งชื่อในวงเล็บ
    plt.plot(xUsage,yCPUUsage) # คำสั่งวาดกราฟ
    plt.plot(xUsage,yMemoryUsage) # คำสั่งวาดกราฟ

    ax = plt.gca()
    ax.set_title(u'Monitor CPU & RAM in process',fontname='Tahoma',fontsize=13)
    ax.legend([u'CPU in process',u'Memory in process'])
    plt.suptitle('Process')
    plt.show()

if __name__ == "__main__":
    from multiprocessing import Process
    with codecs.open("output/25kb 3889 test golang_monitor.json",'r',encoding="utf-8") as file:
        data = file.read()
        jsonData = json.loads(data)
    monitor = jsonData["monitor"]

    procs = []
    p2 = Process(target=plotProcess, args=(monitor,))
    p2.start()
    procs.append(p2)
    p1 = Process(target=plotSystem,args=(monitor,))
    p1.start()
    procs.append(p1)
    for p in procs:
        p.join()

