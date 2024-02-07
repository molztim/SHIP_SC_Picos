#An examplary sensor/device
from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin, I2C
from MPU6050 import *
import math


class device:

    def __init__(self,rtc):
        try:
            self.rtc = rtc          #The rtc
            self.ID = "TILT SENSOR 10.42.0.130"
            self.IP = '10.42.0.130'
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.cal_angle = 0.0           #Main data 
            self.angle = 0.0
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel

            self.angle_offset = 0.0
            self.calib_vec = [0.9958471, -0.005946045, 0.09761597]

            try:
                self.cal_angle, self.angle_offset = config_reader()
            except:
                log("Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration")
            
            self.i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
            init_mpu6050(self.i2c)
            log("Device Up!")

        except:
            raise RuntimeError("Error 01: Init error")
        
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    
    def measurement(self):
        while self.runFlag:
            vec = []
            n = 3
            start = utime.ticks_ms()
            for i in range(n):
                vec += [list(get_mpu6050_data(self.i2c)['accel'].values())]

            vec = list(map(list, zip(*vec)))
            avg_vec = [sum(x)/n for x in vec]
            
            rad = sum([a*b for a,b in zip(self.calib_vec,avg_vec)])/(math.sqrt(sum([a**2 for a in self.calib_vec]))*math.sqrt(sum([b**2 for b in avg_vec])))
            if rad == 1.0:
                self.angle = 0.00
            elif rad == -1.0:
                self.angle = 180
            else:
                self.angle = math.acos(rad)*180/math.pi + self.angle_offset
            stop = utime.ticks_ms()
            print(f"Data: {self.angle}, {self.angle_offset}, {utime.ticks_diff(stop,start)}")
            

    def server(self,received):
        if "GET" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            self.cal_angle = self.angle - self.angle_offset
            self.read_flag = False

            #Now we gan return the data
            return f"{self.cal_angle:.2f},{self.angle_offset:.2f}"
        
        elif "SET" in received:
            newOffset = float(received.split(" ")[1])
            if "ROT" in received:
                self.angle_offset = self.angle - newOffset

            config_writer(self.rtc,[self.cal_angle, self.angle_offset])
            return "INTERNAL"
        else:
            return "A"
        
    def kill(self):
        self.runFlag = False
        gc.collect()
        _thread.exit()
