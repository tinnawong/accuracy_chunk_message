from guppy import hpy
import psutil,time,sys
import psutil,os
import platform,codecs
from prove import generateMatrix
print(platform.system())
# you can convert that object to a dictionary 
print("ram :",dict(psutil.virtual_memory()._asdict()))
# you can have the percentage of used RAM
print("swap memory :",psutil.swap_memory()._asdict())

print(os.getpid())
time.sleep(10)
p = psutil.Process(os.getpid())
# with codecs.open("output\output_prove.json","r",encoding="utf-8") as f:
#     tt = f.read()
# print(p.children())
print("memory usage :",p.memory_info()._asdict()["rss"]*0.000001)
