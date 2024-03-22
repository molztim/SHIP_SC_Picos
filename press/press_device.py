#An examplary sensor/device
from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin,I2C,ADC


class device:

    def __init__(self,rtc):
        try:
            self.rtc = rtc          #The rtc
            self.ID = "SCINTILLATOR PRESSURE 10.42.0.145"
            self.IP = '10.42.0.145'
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.data = 0           #Main data 
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel
            self.press_offset = 0.0        
            self.pressure = 0.0
            self.cal_pressure = 0.0   


            self.ohm = 150 #Ohm
            self.adc_offset = 310 #mA
            self.low = 4 #mA
            self.high = 20 #m!
            self.v_low = self.low * self.ohm / 1000 #mV
            self.v_high = self.high * self.ohm / 100 #mV
            self.adc_steps = 3.3/(2**12) #ADC/V

            self.density = 863 #kg/m³
            self.g = 9.81 #m/s²
            self.level = 0
            self.level_offset = 0



            try:
                self.cal_pressure,self.press_offset = config_reader()
            except:
                log("Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration")

            self.adc0 = ADC(0)
            log("Device Up!")

        except:
            raise RuntimeError("Error 01: Init error")
        
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    
    def measurement(self):
        while self.runFlag:
            avg_adc = 0
            n = 100
            start = utime.ticks_ms()
            for i in range(n):
                avg_adc += (self.adc0.read_u16()>>4) / n 
            measV = avg_adc*self.adc_steps
            self.pressure = ((measV / self.ohm * 1000) - self.low)/16 * 1000 #mbar
            stop = utime.ticks_ms()
            self.level = self.pressure * 1e5 / (self.g*self.density) #mm

            print(f"Data: {self.pressure} {utime.ticks_diff(stop,start)}")
            

    def server(self,received):
        if "GET" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            self.cal_pressure = (self.pressure - self.press_offset)
            self.read_flag = False

            #Now we gan return the data
            return f"{self.cal_pressure:.0f},{self.level:.0f}"
        
        elif "SET" in received:
            newOffset = float(received.split(" ")[1])
            if "PRESS" in received:
                self.press_offset = self.pressure - newOffset
            elif "LEVEL" in received:
                self.level_offset = self.level - newOffset
            config_writer(self.rtc,[self.cal_pressure,self.press_offset])
            return "INTERNAL"
        else:
            return "A"
        
    def kill(self):
        self.runFlag = False
        gc.collect()
        _thread.exit()
