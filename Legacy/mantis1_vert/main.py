
##### LASER 1 ####

import network
import socket
import binascii
import ubinascii
import utime as time

from micro_wlan import t_wlan
from machine import Pin, I2C
from laserserver import laserserver
from laserreangefinder import laserrangefinder

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

from time import localtime as lt
def log(*service_string):
    output = "{:02d}:{:02d}:{:02d}|".format(*lt()[3:6])
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
IP = ('10.42.0.142','255.255.255.0', '10.42.0.1', '10.42.0.1')

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

f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [int(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
calib,laserstatus,lastdata,fast = contentlist
log("Calibration Geladen!")

#calib = 0
#laserstatus = True
#lastdata = 0
#fast = 0 #Toggles Fast readout mode
fast_counter = 0
fast_limit = int(60/2 * 1) #last number in minutes, 2 due to readout time intervall of 2s
modecontrol = 1

log("Starting UART...")
laser = laserrangefinder()
#This line is required to start the laser
if laserstatus:
    laser.laserON()

log("Loading done - ready for operations\n")

led_pin = Pin(LED, Pin.OUT,value=1)

while True:
    cl, addr = s.accept()
    while True:
        try:
            #log('client connected from', addr)
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            log("Received bytes: ",rcv)
               
            response = laserserver(rcv,laser,calib,lastdata,laserstatus,modecontrol,fast)
            
            #This is to count up when not fast mode is enganged
            if fast == 1:
                modecontrol = 1
                fast_counter = 0
            elif fast_counter == fast_limit:
                modecontrol = 1
                fast_counter = 0
                log("Limit Reached, next will be read")
            else:
                modecontrol = 0
                fast_counter+=1
                
            log("Response: ",response)
            
            if "INTERNAL" in response:
                answer = response.split(":")
                if "DIST" in rcv:
                    calib = int(answer[1]) - int(answer[2])
                    log(f"Calibration Distance: {calib}")
                elif "STAT" in rcv:
                    laserstatus = answer[-1]
                    log(f"Laserstatus set to: {laserstatus}")
                elif "MODE" in rcv:
                    fast = answer[-1]
                    log(f"FAST Mode set to: {fast}")
                #Log new setup    
                logsetting([calib,laserstatus,int(lastdata),fast])
                
            else:
                if "DIST" in rcv:
                    lastdata = float(response)
                size = cl.send(response+'\r')
                #log(f"Package of size {size} send")
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(3)
            break

