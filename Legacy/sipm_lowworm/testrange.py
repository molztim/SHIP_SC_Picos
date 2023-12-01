import network
import socket
import binascii
import ubinascii
import utime as time
import pickle

from micro_wlan import t_wlan
from machine import Pin, I2C
from SHiPserver import webserver,timetest

from I2C.i2c_caen import A7585
from spi import eMUSIC

#Ports
I2C_SDA = 4
I2C_SCL = 5
I2C_ENA = 22
LED = "LED"
I2C_A0 = 19
I2C_A1 = 20

# Pin Init
enable_Pin = Pin(I2C_ENA, Pin.OUT, value=0)
A0 = Pin(I2C_A0,Pin.OUT, value=1)
A1 = Pin(I2C_A1,Pin.OUT, value=1)


TMP37 = [0,20,0] #V, V, V
DEV = A7585(112,I2C_SDA,I2C_SCL)
DEV.startup(80,10,20,2,rampuptime=2)
DEV.SetTemperatureSensor("CUSTOM", *TMP37)
#DEV.SetSIPMtcoef(34/1000)

#EMUSIC = eMUSIC(17,18,16,19)
#init_calib = EMUSIC.read_calib()
#EMUSIC.write_config(init_calib)

print("Loading done - ready for operations\n")

delay = 3

print("PING!")
while True:
    temp = DEV.GetTref()
    v_correct = DEV.GetVcorrection()
    print(f"{temp} °C {v_correct} mV")
    time.sleep(2)
    
    
