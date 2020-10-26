

import psutil,time,sys,os

# you can convert that object to a dictionary 
print("ram :",dict(psutil.virtual_memory()._asdict()))
# you can have the percentage of used RAM
print("swap memory :",psutil.swap_memory()._asdict())


while(1):
    p = psutil.Process(13664) 
    print("memory usage :",p.memory_info()._asdict())
    print("cpu :",p.cpu_percent())
    with p.oneshot():
        print(p.name())  # execute internal routine once collecting multiple info
        print(p.cpu_times())  # return cached value
        print(p.cpu_percent())  # return cached value
        print(p.create_time() ) # return cached value
        print(p.ppid())  # return cached value
        print(p.status())  # return cached value
    time.sleep(1)
    