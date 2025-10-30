
from machine import UART, Pin
from pico_utils import *
import time

def CS(data):
    return (~sum(data) + 1) & 0xFF

LASER_ON = [0x80, 0x06,0x05,0x01,0x74]
LASER_OFF = [0x80,0x06,0x05,0x00,0x75]

STAND_FREQ = [0xFA, 0x0A,0x00,0xF8]
LOW_FREQ = [0xFA, 0x0A,0x05,0xF3]
MED_FREQ = [0xFA, 0x0A,0x0A,0xEE]
HI_FREQ = [0xFA, 0x0A,0x14,0xE4]

MEA_INTER = [0xFA, 0x04, 0x05,0xFF, CS([0xFA, 0x04, 0x05,0xFF])]

ADDR = 0x80
SIN_MEAS = [ADDR,0x06,0x02, CS([ADDR,0x06,0x02])]
CON_MEAS = [ADDR,0x06,0x03, CS([ADDR,0x06,0x03])]

SET_RES_1MM = [0xFA,0x04,0x0C, 0x01, CS([0xFA,0x04,0x0C, 0x01])]
SET_RES_01MM = [0xFA,0x04,0x0C, 0x02, CS([0xFA,0x04,0x0C, 0x02])]

SHUTDOWN = [0x80,0x04,0x02,0x7A]


class laserrangefinder():
    def __init__(self,tx=0,rx=1):
        self.uart = UART(0, baudrate=9600,  bits = 8, parity = None, stop = 1,tx=Pin(tx), rx=Pin(rx),timeout=100)
        return None
    
    def uart_raw(self,l=1):
        return self.uart.read()

    
    def read(self):
        if self.uart.any():
        #if True:
            rxData = self.uart.read(64)
            #print(rxData)
            if rxData:
                if len(rxData) == 11:
                    # We run at 1mm resolution, so we have to think, that ddd.ddd is in 1.0mm
                    distance = float("".join([chr(x) for x in rxData[3:-1]]))*1000
                    #print(i,distance)
                    return distance

            
        
    def laserON(self):
        self.uart.write(bytearray(CON_MEAS))
        return 1
    
    def laserOFF(self):
        self.uart.write(bytearray(SHUTDOWN))
        return 0
    
    def laserstop(self):
        print("Deinit UART")
        self.uart.deinit()
    



