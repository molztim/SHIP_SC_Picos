import network
import socket
import binascii
import ubinascii
import utime as time

from micro_wlan import t_wlan
from machine import Pin,I2C,ADC
from readout import pressure_readout,level_readout
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
IP = ('10.42.0.133','255.255.255.0', '10.42.0.1', '10.42.0.1')

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

#offsets
delta_off = 0
press_off = 0
level_off = 0

#Loading Offsets
f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [int(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
delta_off, press_off, level_off = contentlist
log("Calibration Loaded!")

#Start adc
adc0 = ADC(0)

log("Loading done - ready for operations\n")

while True:
    cl, addr = s.accept()
    while True:
        try:
            #log('client connected from', addr)
            #RCV data
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            log("Received bytes: ",rcv)
            #if rcv == "":
            #    raise Exception("Nothing found")
            
            #Analyze Instructions and send back(adjust offset
            if "GET" in rcv:
                if "PRES" in rcv:
                    response = "{:.2f}".format(pressure_readout(adc0)*1000) #mbar
                elif "LEVEL" in rcv:
                    response = "{:.0f}".format(level_readout(adc0)*100)   #cm             
                elif "DELTA" in rcv:
                    response = "{:.2f}".format(0)
                else:
                    response = "8000"
                cl.send(response+'\r')
            elif "SET" in rcv:
                value = float(rcv.split(" ")[-1])
                if "PRESS" in rcv:
                    press_off = float(pressure_readout(adc0)) - value
                elif "LEVEL" in rcv:
                    delta_off = float(level_readout(adc0)) - value
                elif "DELTA" in rcv:
                    delta_off = float(0) - value
                else:
                    None
                logsetting(press_off,deltas_off,level_off)
               

            log("Response: ",response)
        except Exception as e:
            #What happens if stuff breaks
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(3)
            break
