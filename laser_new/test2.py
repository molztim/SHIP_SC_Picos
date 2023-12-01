from micro_wlan import t_wlan
from machine import Pin, I2C
from laserreangefinder import *
import utime as time
import _thread

CON_MEAS = [ADDR,0x06,0x03, CS([ADDR,0x06,0x03])]


laserdata = 0

I2C_SDA = 0
I2C_SCL = 1
LED = "LED"
LASER_POWER = Pin(2, Pin.OUT,value=1)
tx=0
rx=1

print("Starting UART...")

#uart = UART(0, baudrate=9600,  bits = 8, parity = None, stop = 1,tx=Pin(tx), rx=Pin(rx))
#uart.write(bytearray(CON_MEAS))


def read3():
    rxData = b'\x80\x06\x83000.324\xa0'
    print(len(rxData))
    while True:
        if rxData is not None and len(rxData) > 10:
            break
    print(rxData)
    snippets = rxData.split(b'\x80')[::-1]
    for snippet in snippets:
        print(snippets,len(snippet))
        if len(snippet) == 10:
            asciiList = [chr(e) for e in snippet[3:-1]]
            print("Snippet: ",snippet)
            print("ASCII: ",asciiList)
            floatdistance = float("".join(asciiList))
            print(floatdistance * 1000)
            return floatdistance
        else:
            None

read3()