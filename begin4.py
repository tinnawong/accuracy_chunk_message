import codecs,json
import matplotlib.pyplot as plt
import os

def plotSystem(monitor):
    yMemoryUsage = []
    yCPUUsage = []
    checkPoint = False
    for i,logProcess in enumerate(monitor):
        if("process" in logProcess):
            if(not checkPoint):
                startTime = i
                checkPoint = True
        else:
            pass
        yCPUUsage.append(logProcess["psutil_cpu_percent"])
        yMemoryUsage.append(logProcess["psutil_virtual_memory"]["percent"])

        
    xMemoryUsage = [x for x in range(startTime,len(yMemoryUsage)+startTime)]
    yBeforCPU = [x["psutil_cpu_percent"] for x in monitor[:10]]

    xBeforCPU = [x for x in range(10)]

    yCPU = [x["psutil_cpu_percent"] for x in monitor[9:len(monitor)-10]]
    xCPU = [x for x in range(9,len(monitor)-10)]

    pyMemory  = [x["psutil_virtual_memory"]["percent"] for x in monitor]

    # กำหนดค่าของ x และ y ที่จะใช้
    x = range(0,len(monitor),1)
    plt.xlabel('time(s)')   #แกน x พร้อมตั้งชื่อในวงเล็บ
    plt.ylabel('percent(%)')   #แกน y พร้อมตั้งชื่อในวงเล็บ
    plt.plot(xCPU,yCPU) # คำสั่งวาดกราฟ
    plt.plot(x,pyMemory) # คำสั่งวาดกราฟ
    plt.plot(xBeforCPU,yBeforCPU)
    # plt.show() # คำสั่งให้แสดง

    ax = plt.gca()
    ax.set_title(u'Monitor CPU & RAM',fontname='Tahoma',fontsize=13)
    # ax.plot(x,take,'-om')
    # ax.plot(x,ono,'-oc')
    # ax.plot(x,fuku,'-oy')
    ax.legend([u'CPU',u'Memory'])
    plt.show()

def plotProcess(monitor):
    yMemoryUsage = []
    yCPUUsage = []
    checkPoint = False
    for i,logProcess in enumerate(monitor):
        if("process" in logProcess):
            if(not checkPoint):
                startTime = i
                checkPoint = True
            # print(logProcess["process"]["cpu_percent"])
            yMemoryUsage.append(logProcess["process"]["memory_percent"])
            yCPUUsage.append(logProcess["process"]["cpu_percent"])
    xMemoryUsage = [x for x in range(startTime,len(yMemoryUsage)+startTime)]    

    plt.xlabel('time(s)')   #แกน x พร้อมตั้งชื่อในวงเล็บ
    plt.ylabel('percent(%)')   #แกน y พร้อมตั้งชื่อในวงเล็บ
    plt.plot(xMemoryUsage,yCPUUsage) # คำสั่งวาดกราฟ
    plt.plot(xMemoryUsage,yMemoryUsage) # คำสั่งวาดกราฟ

    ax = plt.gca()
    ax.set_title(u'Monitor CPU & RAM in process',fontname='Tahoma',fontsize=13)
    ax.legend([u'CPU in process',u'Memory in process'])
    plt.show()

if __name__ == "__main__":
    from multiprocessing import Process
    with codecs.open("output/10kb 3911 test_monitor.json",'r',encoding="utf-8") as file:
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

