
from micro_wlan import t_wlan
from machine import Pin, I2C
from laserreangefinder import *
import utime as time
import _thread

ADDR = 0x80
SIN_MEAS = [ADDR,0x06,0x02, CS([ADDR,0x06,0x02])]
CON_MEAS = [ADDR,0x06,0x03, CS([ADDR,0x06,0x03])]


laserdata = 0

I2C_SDA = 0
I2C_SCL = 1
LED = "LED"
LASER_POWER = Pin(2, Pin.OUT,value=1)
tx=0
rx=1

print("Starting UART...")

uart = UART(0, baudrate=9600,  bits = 8, parity = None, stop = 1,tx=Pin(tx), rx=Pin(rx))




while True:
    uart.write(bytearray(SIN_MEAS))
    rxData = None
    while rxData == None:
        rxData = uart.read(20)
        if rxData is not None:
            rxData = rxData.split(b'\x80')
            for i in range(len(rxData)):
                try:
                    snippet = rxData[-i]
                    asciiList = [chr(e) for e in snippet[3:-1]]
                    floatdistance = float("".join(asciiList))
                    print(f"Float: {floatdistance}")
                    break
                except:
                    continue
            break
    time.sleep(1)




