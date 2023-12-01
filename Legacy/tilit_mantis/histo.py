from machine import Pin, I2C
import utime as time
from mpu6050 import init_mpu6050, get_mpu6050_data
import math

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
init_mpu6050(i2c)

acceldata = get_mpu6050_data(i2c)['accel']['y']
histo =  [[x,0] for x in range(-15,16)]

n = 200
factor = 1000

for i in range(0,n):
    masterbreak = True
    newMeas = get_mpu6050_data(i2c)['accel']['y']
    diff = newMeas - acceldata
    acceldata = newMeas
    for i in range(len(histo)):
        if diff*factor >= histo[i][0]:
            continue
        else:
            histo[i][1]+= 1
            masterbreak = False
            break
    if masterbreak:
        histo[-1][1]+= 1
    
#print(f"Histo: {histo}")
    
summe = 0
for e in histo:
    summe += e[1]
    #print(f"> {e[0]/factor} - "+"*"*round(e[1]))
    
print(f"Summe: {summe}")

gauss_right_side = 15.85 #%
total_count_limit = round(n * 15.85/100)

total_count = 0
for e in histo:
    old_count = total_count
    total_count += e[1]
    if total_count > total_count_limit:
        count_difference = total_count - old_count
        diff_to_limit = total_count_limit - old_count
        percentage = diff_to_limit/count_difference
        point = percentage*(e[0]-1) + (1-percentage)*(e[0])
        print(f"Found {total_count} of {total_count_limit} ({total_count/n*100}% at {e[0]/factor}), where {percentage} is in the bin {e[0]}.")
        print(f"From that: {percentage} means that the point is {abs(point)/factor}")
        break
    
    
