from time import sleep
import time
from machine import UART, Pin

#from laserreangefinder import *

def CS(data):
    return (~sum(data) + 1) & 0xFF

ADDR = 0x80
SIN_MEAS = [ADDR,0x06,0x02, CS([ADDR,0x06,0x02])]
CON_MEAS = [ADDR,0x06,0x03, CS([ADDR,0x06,0x03])]

uart = UART(0, baudrate=9600,  bits = 8, parity = None, stop = 1,tx=Pin(0), rx=Pin(1))

SHUTDOWN = [0x80,0x04,0x02,0x7A]
   
#uart.write(bytearray(SHUTDOWN))



def uartreader(l,start = 128):
        message_lenght = 0
        data = []
        while len(data) < l:
            rxData = uart.read(1)
            if rxData == None:
                continue
            elif rxData == b'\x80':
                data = []
                data += [int.from_bytes(rxData, "big")]
                #print("Last entry:",data[-1])

            elif len(data) > 0:
                data += [int.from_bytes(rxData, "big")]
                #print("Last entry:",data[-1])
            else:
                #print("Waiting for good stuff...",rxData)
                continue
            
            sleep(0.001)
        return data
  

for i in range(2):
    uart.write(bytearray(CON_MEAS))
    for i in range(5):
        rxData = uartreader(11)
        print(rxData)
        sleep(1)
        schrottData = uart.readline()
        

    uart.write(bytearray(SHUTDOWN))
    print("Finished Operation")
    sleep(1)



#while True:
#start = time.ticks_us()
    #uart.write(bytearray(SIN_MEAS))
    #rxData = uartreader(11)
    #asciiList = [chr(e) for e in rxData[3:-1]]
    #floatdistance = float("".join(asciiList))
#stop = time.ticks_us()
    #print(f"Distance {rxData}m")
    #sleep(0.3)
#print(time.ticks_diff(stop, start)/1000)

