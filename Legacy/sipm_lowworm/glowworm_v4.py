#Ports
I2C_SDA = 4
I2C_SCL = 5
I2C_ENA = 22
LED = "LED"
I2C_A0 = 19
I2C_A1 = 20

#Network parameter
SSID = "SHIP_PicoNet"
PASS = "ThereIsAlwaysABiggerFish"
IP = ('10.42.0.125','255.255.255.0', '10.42.0.1', '10.42.0.1')
#SSID = "piwpa2"
#PASS = "pascalKrankenhaus"
#SSID ="PicoNetwork"
#PASS = "youshallnotpass"

#EMUSIC_CONFIG = [1, 144, 144, 111, 120, 3, 6, 3, 15, 0, 3, 0, 0, 3, 0, 38, 31, 3, 15, 3, 4, 4, 25, 3, 1, 0, 244, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 236, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 228, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 224, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 232, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 229, 1, 1, 1, 1, 120, 1, 0, 1] 

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

from time import localtime as lt
def log(*service_string):
    output = "{}:{}:{} | ".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None



# Pin Init
led = Pin(LED, Pin.OUT, value=1)
enable_Pin = Pin(I2C_ENA, Pin.OUT, value=0)
A0 = Pin(I2C_A0,Pin.OUT, value=1)
A1 = Pin(I2C_A1,Pin.OUT, value=1)

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
#s.bind(addr)
s.bind(('',80))
s.listen(5)
print('listening on', addr)

#I2C Init
DEV = A7585(112,I2C_SDA,I2C_SCL)
DEV.startup(80,10,30,2,rampuptime=2)
enable_Pin.value(1)

#eMUSIC SPI
EMUSIC = eMUSIC(17,18,16,19)
print("I2C ready!")

init_calib = EMUSIC.read_calib()
EMUSIC.write_config(init_calib)
#Data Dummy
data_string = "GW1"

# Listen for connections
log("Loading done - ready for operations\n")

#Create new Socket for communication
while True:
    cl, addr = s.accept()
    while True:
        try:
            
            
            #log('client connected from', addr)
            package = cl.recv(256)
            rcv = package.decode('utf-8')
            end_wait = time.ticks_us()
            start = time.ticks_us()
            log("Received bytes: ",rcv)
               
            response = webserver(rcv,DEV,EMUSIC,enable_Pin) +'\r'
            log("Response: ",response)
            
            #Send response
            res = time.ticks_us()
            size = cl.send(response)
            log(f"Package of size {size} send")
            end_res = time.ticks_us()
            
            #led.toggle()
            
            
            end = time.ticks_us()
            try:
                diff_wait = time.ticks_diff(end_wait,start_wait)/1000
                print(f"Waited for command: {diff_wait} ms.")
            except:
                None
            diff = time.ticks_diff(end,start)/1000
            print(f"Time for entire process: {diff} ms.")
            res_diff = time.ticks_diff(res,end_res)/1000
            print(f"Time to send Response: {res_diff} ms.\n")
            start_wait = time.ticks_us()
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            log("Close interaction with: {}\n".format(e))
            time.sleep(3)
            break
 



