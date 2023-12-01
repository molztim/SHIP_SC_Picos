from machine import UART, Pin
from time import sleep
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
        self.uart = UART(0, baudrate=9600,  bits = 8, parity = None, stop = 1,tx=Pin(tx), rx=Pin(rx))
        return None
    
    def uart_raw(self,l=1):
        return self.uart.read(l)
    
    def uartreader(self,l,start = 128):
        message_lenght = 0
        data = []
        while len(data) < l:
            rxData = self.uart.read(1)
            if rxData == None:
                continue
            elif rxData == b'\x80':
                data = []
                data += [int.from_bytes(rxData, "big")]
                #print("\nFirst entry: ",data[-1]," ",end="")

            elif len(data) > 0:
                data += [int.from_bytes(rxData, "big")]
                #print(data[-1]," ",end="")
            else:
                #print("Waiting for good stuff...",rxData)
                continue
            
            #sleep(0.001)
            time.sleep_us(1)
        #print("Final List:",data)
        return data
    
    def read(self):
        rxData = self.uartreader(11)
        asciiList = [chr(e) for e in rxData[3:-1]]
        floatdistance = float("".join(asciiList))
        
        return floatdistance
    
    def read2(self):
        rxData = None
        while rxData == None:
            rxData = self.uart.read(250)
            if rxData is not None:
                rxData = rxData.split(b'\x80')
                for i in range(len(rxData)):
                    try:
                        snippet = rxData[-i]
                        asciiList = [chr(e) for e in snippet[3:-1]]
                        floatdistance = float("".join(asciiList))
                        #print(f"Float: {floatdistance}")
                        return floatdistance
                    except:
                        continue
                break
            else:
                None
                
    def read3(self):
        while True:
            rxData = self.uart.read()
            while True:
                if rxData is not None and len(rxData) > 10:
                    break
            #print(rxData)
            snippets = rxData.split(b'\x80')[::-1]
            for snippet in snippets:
                #print(snippets,len(snippet))
                if len(snippet) == 10:
                    asciiList = [chr(e) for e in snippet[3:-1]]
                    #print("Snippet: ",snippet)
                    #print("ASCII: ",asciiList)
                    floatdistance = float("".join(asciiList))
                    #print(floatdistance * 1000)
                    return floatdistance
                else:
                    None
            

        
    def laserON(self):
        self.uart.write(bytearray(CON_MEAS))
        return 1
    
    def laserOFF(self):
        self.uart.write(bytearray(SHUTDOWN))
        return 0
    

