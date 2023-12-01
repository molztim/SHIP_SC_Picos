#Ports
LED = "LED"
SDA = 20
SCL = 21

#Network parameter
SSID = "SHIP_PicoNet"
PASS = "ThereIsAlwaysABiggerFish"
IP = ('10.42.0.130','255.255.255.0', '10.42.0.1', '10.42.0.1')
#SSID = "piwpa2"
#PASS = "pascalKrankenhaus"
#SSID ="PicoNetwork"
#PASS = "youshallnotpass"

import network
import socket
import binascii
import ubinascii
import utime as time

from micro_wlan import t_wlan
from machine import Pin, I2C

from mpu_readout import gyro_server
from mpu6050 import *

from time import localtime as lt
def log(*service_string):
    output = "{}:{}:{} | ".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None



# Pin Init
led = Pin(LED, Pin.OUT, value=1)

if True:
    time.sleep(0.2)
    led.toggle()
    time.sleep(0.2)
    led.toggle()
print("System up...")

#Login to Wifi
wlan_ips = t_wlan(SSID,PASS,IP)
print("Device IP:",wlan_ips[0],"\n")
time.sleep_ms(100)

#Start Server socket
addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
s = socket.socket()
s.bind(('',80))
s.listen(5)
print('listening on', addr)

#Data Dummy
data_string = "DF1"
#Zeros:
calib_angle = 0

log("Starting I2C...")
i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
init_mpu6050(i2c)
calib_vec = angle_zeroing(i2c,50)
log("Loading done - ready for operations\n")

#Create new Socket for communication
while True:
    cl, addr = s.accept()
    while True:
        try:
            #log('client connected from', addr)
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            log("Received bytes: ",rcv)        
            response = gyro_server(rcv,i2c,calib_angle,calib_vec)
            log("Response: ",response)
            if "INTERNAL" in response:
                newCalib = response.split(":")
                calib_angle = float(newCalib[1]) - float(newCalib[2])
                log(f"Calibration Angle: {calib_angle}")
            else:
                size = cl.send(response+'\r')
                log(f"Package of size {size} send")

        except Exception as e:
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(2)
            break
 




