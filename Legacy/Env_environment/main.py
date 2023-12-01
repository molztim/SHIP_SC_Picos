import network
import socket
import binascii
import ubinascii
import utime as time

from micro_wlan import t_wlan
from machine import Pin, I2C
import bme280 as BME280

from machine import RTC
rtc = RTC()

from time import localtime as lt
def log(*service_string):
    output = "{}:{}:{} | ".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None

def logsetting(contentlist):
    f = open("lastconfig.txt","a")
    now = rtc.datetime()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    body = ','.join(str(e) for e in contentlist)
    print(head,body)
    f.write("\n"+head+body)
    f.close()
    return None

SSID = "SHIP_PicoNet"
PASS = "ThereIsAlwaysABiggerFish"
IP = ('10.42.0.144','255.255.255.0', '10.42.0.1', '10.42.0.1')

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

#Start BME
i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
bme = BME280.BME280(i2c=i2c)

#Loading Offsets
f = open("env_lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [int(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
temp_offset,pres_offset,hum_offset = contentlist
log("Calibration Loaded!")

#temp_offset = 0
#pres_offset = 0
#hum_offset = 0

log("Loading done - ready for operations\n")

led = Pin("LED", Pin.OUT, value=1)


while True:
    cl, addr = s.accept()
    while True:
        try:
            #log('client connected from', addr)
            #RCV data
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            log("Received bytes: ",rcv)
            
            #Analyze Instructions and send back(adjust offset
            if "GET" in rcv:
                if "TEMP" in rcv:
                    response = "{}".format(float(bme.temperature) - temp_offset) 
                elif "PRESS" in rcv:
                    response = "{}".format(float(bme.pressure) - pres_offset)
                elif "HUM" in rcv:
                    response = "{}".format(float(bme.humidity) - hum_offset)
                else:
                    response = "8000"
                cl.send(response+'\r')
            elif "SET" in rcv:
                value = float(rcv.split(" ")[-1])
                if "TEMP" in rcv:
                    temp_offset = float(bme.temperature) - value
                elif "PRESS" in rcv:
                    pres_offset = float(bme.pressure) - value
                elif "HUM" in rcv:
                    hum_offset = float(bme.humidity) - value
                else:
                    None
                logsetting(temp_offset,pres_offset,hum_offset)
               

            log("Response: ",response)
            
            if rcv == "":
                print("Connection closed")
                break
        except Exception as e:
            #What happens if stuff breaks
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(3)
            break
