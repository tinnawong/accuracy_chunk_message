import codecs,json
import matplotlib.pyplot as plt

with codecs.open("output/monitor_25kb 3889 test.json",'r',encoding="utf-8") as file:
    data = file.read()
    jsonData = json.loads(data)
monitor = jsonData["monitor"]

pyCPU = [x["psutil_cpu_percent"] for x in monitor]
pyMemory  = [x["psutil_virtual_memory"]["percent"] for x in monitor]

# กำหนดค่าของ x และ y ที่จะใช้
x = range(0,len(monitor)*2,2)
plt.xlabel('time(s)')   #แกน x พร้อมตั้งชื่อในวงเล็บ
plt.ylabel('percent(%)')   #แกน y พร้อมตั้งชื่อในวงเล็บ
plt.plot(x,pyCPU) # คำสั่งวาดกราฟ
plt.plot(x,pyMemory) # คำสั่งวาดกราฟ
# plt.show() # คำสั่งให้แสดง


ax = plt.gca()
ax.set_title(u'Monitor CPU & RAM',fontname='Tahoma',fontsize=13)
# ax.plot(x,take,'-om')
# ax.plot(x,ono,'-oc')
# ax.plot(x,fuku,'-oy')
ax.legend([u'CPU',u'Memory'])
plt.show()