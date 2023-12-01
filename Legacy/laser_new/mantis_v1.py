import network
import socket
import binascii
import ubinascii
import utime as time

from micro_wlan import t_wlan
from machine import Pin, I2C
from lidarserver import lidarserver
from laserserver import laserserver
from laserreangefinder import laserrangefinder

from time import localtime as lt
def log(*service_string):
    output = "{}:{}:{} | ".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None

I2C_SDA = 0
I2C_SCL = 1
LED = "LED"
LASER_POWER = Pin(2, Pin.OUT,value=1)



SSID = "SHIP_PicoNet"
PASS = "ThereIsAlwaysABiggerFish"
IP = ('10.42.0.131','255.255.255.0', '10.42.0.1', '10.42.0.1')

#Login to Wifi
wlan_ips = t_wlan(SSID,PASS,IP)
print("Device IP:",wlan_ips[0],"\n")
time.sleep_ms(100)

#Start Server socket
addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
s = socket.socket()
#s.bind(addr)
s.bind(('',80))
s.listen(5)
print('listening on', addr)


#Server done, now ocme to Laser Rangefinder
calib = 0
laserstatus = True
lastdata = 0

log("Starting UART...")
laser = laserrangefinder()
#This line is required to start the laser
if laserstatus:
    laser.laserON()

log("Loading done - ready for operations\n")

while True:
    cl, addr = s.accept()
    while True:
        try:
            #log('client connected from', addr)
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            log("Received bytes: ",rcv)
               
            response = laserserver(rcv,laser,calib,lastdata,laserstatus)
            log("Response: ",response)
            
            if "INTERNAL" in response:
                answer = response.split(":")
                if "DIST" in rcv:
                    calib = int(answer[1]) - int(answer[2])
                    log(f"Calibration Distance: {calib}")
                elif "STAT" in rcv:
                    laserstatus = answer[-1]
                    log(f"Laserstatus set to: {laserstatus}")
            else:
                lastdata = float(response)
                size = cl.send(response+'\r')
                #log(f"Package of size {size} send")
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(3)
            break