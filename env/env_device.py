#An examplary sensor/device
from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin, I2C
from BME280 import BME280


class device:

    def __init__(self,rtc):
        try:
            self.rtc = rtc          #The rtc
            self.ID = "ENVIRONMENT SENSOR 10.42.0.133"
            self.IP = '10.42.0.133'
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.temp = 0           #Main data 
            self.pres = 0
            self.humi = 0
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel

            self.temp_offset = 0
            self.pres_offset = 0
            self.humi_offset = 0

            self.cal_temp = 0           #Main data 
            self.cal_pres = 0
            self.cal_humi = 0

            try:
                self.cal_temp,  self.cal_pres, self.cal_humi, self.temp_offset, self.pres_offset, self.humi_offset = config_reader()
            except:
                log("Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration")
            
            i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
            self.bme = BME280(i2c=i2c)
            log("Device Up!")

        except:
            raise RuntimeError("Error 01: Init error")
        
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    
    def measurement(self):
        while self.runFlag:
            avg_temp = 0
            avg_pres = 0
            avg_humi = 0
            n = 3
            start = utime.ticks_ms()
            for i in range(n):
                avg_temp += float(self.bme.temperature)/n
                avg_pres += float(self.bme.pressure)/n
                avg_humi += float(self.bme.humidity)/n
            stop = utime.ticks_ms()
            self.temp = avg_temp
            self.pres = avg_pres
            self.humi = avg_humi
            print(f"Data: {self.temp}, {self.pres}, {self.humi} {utime.ticks_diff(stop,start)}")
            

    def server(self,received):
        if "GET" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            data_string = f"{self.temp - self.temp_offset},{self.pres - self.pres_offset},{self.humi - self.humi_offset}"
            self.read_flag = False

            #Now we gan return the data
            return f"{data_string},{self.temp_offset},{self.pres_offset},{self.humi_offset}"
        
        elif "SET" in received:
            newOffset = float(received.split(" ")[1])
            if "TEMP" in received:
                self.temp_offset = self.temp - newOffset
            elif "PRESS" in received:
                self.pres_offset = self.pres - newOffset
            elif "HUM" in received:
                self.humi_offset = self.humi - newOffset

            config_writer(self.rtc,[self.cal_temp,  self.cal_pres, self.cal_humi, self.temp_offset, self.pres_offset, self.humi_offset])
            return "INTERNAL"
        else:
            return "A"
        
    def kill(self):
        self.runFlag = False
        gc.collect()
        _thread.exit()
