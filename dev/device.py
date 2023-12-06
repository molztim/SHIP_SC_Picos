#An examplary sensor/device
from pico_ultis import *

class device:

    def __init__(self,rtc,s,addr):
        self.calibration = 0
        self.rtc = rtc
        self.ip = addr
        self.socket = s
        #self.i2c = ...
        #self.uart = ...
        #self.fast_counter = 0
        #self.fast_limit = int(60/2 * 1) #last number in minutes, 2 due to readout time intervall of 2s
        #self.modecontrol = 1
        
        self.op_flag = False
        self.command = ""
        self.data = 0

        try:
            log("Device Up!")
        except:
            log("Error 01: Init error")
            
    def get_flag(self):
        return self.op_flag
    
    def set_flag(self, status):
        self.op_flag = status
        return None
    
    def set_command(self, command):
        self.command = command
        return None
    
    def get_data(self):
        return self.data

    def server(self):
        while True:
            while not self.op_flag:
                pass
            print("Request: ",self.command)
            response = "8000"
            self.data = response
            self.op_flag = False