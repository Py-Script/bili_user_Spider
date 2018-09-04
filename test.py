import time


a = time.localtime(1430573269)
timeStr=time.strftime("%Y-%m-%d %H:%M:%S", a)
print(timeStr)