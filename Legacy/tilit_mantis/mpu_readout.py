from machine import Pin, I2C
import utime
from mpu6050 import *
import math

def angle_temp(i2c,n,calib_angle,calib_vec): #I2C, How many cycles are recorded, the calib from doberview, the offset from calibration run
    vec = []
    for i in range(n):
        vec += [list(get_mpu6050_data(i2c)['accel'].values())]
    vec = list(map(list, zip(*vec)))
    avg_vec = [sum(x)/n for x in vec]
    
    rad = sum([a*b for a,b in zip(calib_vec,avg_vec)])/(math.sqrt(sum([a**2 for a in calib_vec]))*math.sqrt(sum([b**2 for b in avg_vec])))
    if rad == 1.0:
        angle = 0.00
    elif rad == -1.0:
        angle = 180
    else:
        angle = math.acos(rad)*180/math.pi + calib_angle
    temp =  get_mpu6050_data(i2c)['temp']
    return (angle,temp)

def gyro_server(request,i2c,calib_angle,calib_vec):
    data_string="WARNING"
    response = ""
    n = 50
    data = angle_temp(i2c,n,calib_angle,calib_vec)
    
    if "GET_" in request:
        if request == "GET_XROT":
            xROT = data[0]
            response = "{:.2f}".format(xROT)
        elif request == "GET_YROT":
            yROT = data[0]
            response = "{:.2f}".format(yROT)
        elif request == "GET_ZROT":
            zROT = data[0]
            response = "{:.2f}".format(zROT)
        elif request == "GET_ANGLE":
            response = "{:.1f}".format(data[0])
        elif request == "GET_DRAGONTEMP":
            response = "{:.1f}".format(data[1])
        elif request == "GET_DRAGONFLY":
            response = "{:.2f},{:.2f}".format(data[0],data[1])
    
    elif "SET_" in request:
        if "ROT" in request:
            Rnew = float(request.split(" ")[1])
            response = "INTERNAL:{:.2f}:{:.2f}".format(Rnew,data[0])
    return response