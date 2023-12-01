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
import math

from machine import RTC
rtc = RTC()

def logsetting(contentlist):
    f = open("lastconfig.txt","a")
    now = rtc.datetime()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    body = ','.join(str(e) for e in contentlist)
    print(head,body)
    f.write("\n"+head+body)
    f.close()
    return None

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
log("Starting I2C...")
i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
init_mpu6050(i2c)
calib_vec = angle_zeroing(i2c,200)
log("Loading done - ready for operations\n")

f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [float(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
calib_vec_old = contentlist[:3] #lets just use the caluclated  zero
calib_angle_old = contentlist[3] 
last_data = contentlist[4] #What happens here: Old or last angle becomes new calibration angle

rad = sum([a*b for a,b in zip(calib_vec,calib_vec_old)])/(math.sqrt(sum([a**2 for a in calib_vec]))*math.sqrt(sum([b**2 for b in calib_vec_old])))
if rad <= 1.0:
    calib_angle = 0.00
elif rad >= -1.0:
    calib_angle = 180
else:
    calib_angle = math.acos(rad)*180/math.pi + calib_angle_old

log("Calibration Geladen!")

logsetting(calib_vec+[calib_angle,last_data])

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
                calib_angle = calib_angle + float(newCalib[1]) - float(newCalib[2])
                print(newCalib[1])
                log(f"Calibration Angle: {calib_angle}")
                logsetting(calib_vec+[calib_angle,float(newCalib[2])])
            else:
                last_data = float(response)
                size = cl.send(response+'\r')
                log(f"Package of size {size} send")
                
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(2)
            break
 