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
            self.ID = "LASER SENSOR M1 10.42.0.142"
            self.IP = '10.42.0.142'
            

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
        while self.runFlag:
            avg_distance = 0
            read_once = False
            n = 3
            start = utime.ticks_ms()
            for i in range(n):
                new_read = self.laser.read4()
                if new_read == "LASER_DIED":
                    self.laser.laserOFF()
                    utime.sleep(1)
                    self.laser.laserON()
                else:
                    read_once = True
                    avg_distance += round(new_read*1000 / n)
            stop = utime.ticks_ms()

            if not self.fastlaserflag:
                utime.sleep(5*60 -2)
            while self.read_flag:
                utime.sleep_ms(1)

            if read_once:
                self.data = avg_distance
                print(f"Data: {self.data} {utime.ticks_diff(stop,start)}")
            else:
                self.laser.laserOFF()
                reset()
            
            """
            print("Buffer Core #2:",end="")
            buffer = 0
            for i in range(50):
                buffer += r.randint(0,20)/50
                print(buffer,end=" ")
                utime.sleep_ms(100)

            while self.read_flag:
                utime.sleep_ms(1)
            self.data = buffer
            print("\n\nData: ",self.data,"\n\n")            
            """

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
        _thread.exit()
