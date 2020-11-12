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
    timeBefor = -1
    count = 0
    avgTime = 0
    for i,logProcess in enumerate(monitor):
        if("process" in logProcess):
            if(not checkPoint):
                startTime = i
                checkPoint = True

            # print(logProcess["process"]["cpu_percent"])
            count += 1
            if(timeBefor == -1):
                firsTime = logProcess["timestamp"]
                timeBefor = logProcess["timestamp"]
            else:
                # print(logProcess["timestamp"]-timeBefor)
                timeBefor = logProcess["timestamp"]
            

            yMemoryUsage.append(logProcess["process"]["memory_percent"])
            yCPUUsage.append(logProcess["process"]["cpu_percent"])
            xUsage.append(i)

    if(len(xUsage) == len(yCPUUsage) and len(xUsage) == len(yMemoryUsage)):
        text = ""
        for i,value in enumerate(xUsage):
            # print(value,"\t",yCPUUsage[i],"\t",yMemoryUsage[i])
            text += str(yCPUUsage[i])+"\t"+str(yMemoryUsage[i])+"\n"
        clipboard.copy(text)
    avgTime = (timeBefor-firsTime)/count
    duration = timeBefor-firsTime
    # text2 = ">>> duration :"+str(duration)+"\n>>> avg :"+str(avgTime)
    # clipboard.copy(text2)
    print(">>> duration :",duration)
    print(">>> avg :",avgTime)
    plt.xlabel('time(≈ %.4f s)\n duration : %.2f s'%(avgTime,duration) )  #แกน x พร้อมตั้งชื่อในวงเล็บ
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
    with codecs.open('../output/7th monitor system/golang prove/3391_monitor.json','r',encoding="utf-8") as file:
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

