from machine import Pin, I2C
from mpu6050 import *
from mpu_readout import angle_temp
import time
import math
from machine import RTC
rtc = RTC()
"""

calib_angle = 0
calib_vec = [0.9958471, -0.005946045, 0.09761597]#angle_zeroing(i2c,200)
data = 50
contentlist = calib_vec+[calib_angle,data]
def logsetting(contentlist):
    f = open("lastconfig.txt","a")
    now = rtc.datetime()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    body = ','.join(str(e) for e in contentlist)
    print(head,body)
    f.write("\n"+head+body)
    f.close()
    return None

#logsetting(contentlist)
f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [float(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
calib_vec = contentlist[:3]
calib_angle = contentlist[3]
data = contentlist[4]
print("Calibration Geladen!",calib_vec,calib_angle,data)
"""

f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = lines
print(float(contentlist.split("\n")[-1].split("|")[-1]))