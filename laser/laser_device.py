
#An examplary sensor/device
from pico_utils import *
import gc
import _thread
import utime
import random as r
from laserrangefinder import laserrangefinder
from machine import reset
from pico_utils import *


class device:

    def __init__(self,rtc):
        try:
            self.rtc = rtc          #The rtc
            self.ID = "LASER SENSOR M1 10.42.0.143"
            self.IP = '10.42.0.143'
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.data = 0           #Main data 
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel
            self.laserstatus = 1    #Activate/Deactivate physical laser
            self.fastlaserflag = 1  #Flag to activate fast mode (fast mode means no averaging of distance data)
            self.calib = 0          #Calibration. Please redo calibration when chaning the orientation
            self.orientation = +1   #Either +1 or -1
            self.cal_distance = 0   #Averaged distance

            try:
                self.cal_distance,self.calib,self.laserstatus,self.fastlaserflag,self.orientation = config_reader()
            except:
                log("Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration")

            self.laser = laserrangefinder()

            if self.laserstatus:
                self.laser.laserON()
                log("Laser ON!")
            log("Device Up!")

        except:
            raise RuntimeError("Error 01: Init error")
        
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    
    def measurement(self):
        start = utime.ticks_ms()
        while self.runFlag:
            try:
                distance = self.laser.read()
            except:
                self.laserOFF()
                utime.sleep(1)
                self.self.laserON()
                utime.sleep(1)
                continue
            if distance:
                print(f"Data: {self.data}")
                if not self.read_flag:
                    self.data = distance
                start = utime.ticks_ms()
            else:
                now = utime.ticks_ms()
                diff = utime.ticks_diff(now, start)
                if diff > 10*1000:
                    self.laser.laserOFF()
                    utime.sleep(1)
                    self.laser.laserON()
                    utime.sleep(1)
                    log("Restarted Laser after 10s of no update...")
                    start = utime.ticks_ms()
                    
                
            if self.fastlaserflag:
                utime.sleep_ms(500)
            else:
                utime.sleep(1)           
            
    def server(self,received):
        if "GET" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            self.cal_distance = str(self.orientation*self.data + self.calib)
            self.read_flag = False

            #Now we gan return the data
            return f"{self.cal_distance},{self.laserstatus},{self.fastlaserflag},{self.orientation}"
        
        elif "SET" in received:
            if "DIST" in received:
                newTarget = int(received.split(" ")[1])
                self.calib = newTarget - self.data*self.orientation
            elif "STAT" in received:
                self.laserstatus = int(received.split(" ")[1])
                if self.laserstatus:
                    self.laser.laserON()
                else:
                    self.laser.laserOFF()
            elif "MODE" in received:
                self.fastlaserflag = int(received.split(" ")[1])
            elif "ORIENTATION" in received:
                self.orientation = int(received.split(" ")[1])

            config_writer(self.rtc,[self.cal_distance,self.calib,self.laserstatus,self.fastlaserflag,self.orientation])
            return "INTERNAL"
        else:
            return "A"
        
    def kill(self):
        self.runFlag = False
        gc.collect()
        self.laser.laserstop()
        _thread.exit()
