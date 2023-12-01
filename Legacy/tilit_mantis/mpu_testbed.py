from machine import Pin, I2C
import utime as time
from mpu6050 import *
import math
 
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
init_mpu6050(i2c)

def vec3d(calib_vec,avg_vec):
    up = 0
    asum = 0
    bsum = 0
    for i in range(3):
        up += calib_vec[i]*avg_vec[i]
        asum += calib_vec[i]**2
        bsum += avg_vec[i]**2
    rad = up/(math.sqrt(asum)*math.sqrt(bsum))
    angle = math.acos(rad)*180/math.pi
    return angle

calib_angle = 0

n = 100
m = 100
data = []
for i in range(n):
    data += [list(get_mpu6050_data(i2c)['accel'].values())]
data = list(map(list, zip(*data)))
calib_vec = [sum(x)/n for x in data]
print(f"Calibration vector {calib_vec}")

calib_angle = 0
last_vec = calib_vec

#liste = []

for i in range(100):
    vec = []
    for i in range(m):
        vec += [list(get_mpu6050_data(i2c)['accel'].values())]
    vec = list(map(list, zip(*vec)))
    avg_vec = [sum(x)/m for x in vec]
    #print(avg_vec)
    rad = sum([a*b for a,b in zip(calib_vec,avg_vec)])/(math.sqrt(sum([a**2 for a in calib_vec]))*math.sqrt(sum([b**2 for b in avg_vec])))
    if rad == 1.0:
        angle = 0.00
    elif rad == -1.0:
        angle = 180
    else:
        angle = math.acos(rad)*180/math.pi
    temp =  get_mpu6050_data(i2c)['temp']
    #print("Angle: {:.3f} by {} Readouts, Temp.: {}".format(angle,m,temp))
    #print("Angle difference {}".format(vec3d(last_vec, avg_vec)))
    #liste.append(vec3d(last_vec, avg_vec))
    last_vec = avg_vec
    
    #time.sleep(1)
#print(liste)
