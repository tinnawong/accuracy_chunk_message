import codecs,json
import matplotlib.pyplot as plt
import os
import clipboard

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

def plotProcess2(monitor):
    yMemoryUsage = []
    yCPUUsage = []
    checkPoint = False
    xUsage =[]
    timeBefor = -1
    count = 0
    avgTime = 0
    buffRamUse = []
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
            
            buffRamUse.append(logProcess["process"]["memory_full_info"]["rss"])
            yMemoryUsage.append(logProcess["process"]["memory_full_info"]["rss"])
            yCPUUsage.append(logProcess["process"]["cpu_percent"])
            xUsage.append(i)

    if(len(xUsage) == len(yCPUUsage) and len(xUsage) == len(yMemoryUsage)):
        text = ""
        for i,value in enumerate(xUsage):
            # print(value,"\t",yCPUUsage[i],"\t",yMemoryUsage[i])
            text += str(yCPUUsage[i])+"\t"+str(yMemoryUsage[i])+"\n"
    clipboard.copy(str(max(buffRamUse)))
    avgTime = (timeBefor-firsTime)/count
    duration = timeBefor-firsTime
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
    """
    รันเพื่อดูการทำงานของ cpu และ ram โดยแสดงเป็นกราฟ
    """
    from multiprocessing import Process
    with codecs.open('../output/3517_raw_monitor.json','r',encoding="utf-8") as file:
        data = file.read()
        jsonData = json.loads(data)
    monitor = jsonData["monitor"]

    procs = []
    p2 = Process(target=plotProcess, args=(monitor,))
    p2.start()
    procs.append(p2)
    p3 = Process(target=plotProcess2, args=(monitor,))
    p3.start()
    procs.append(p3)
    
    for p in procs:
        p.join()

