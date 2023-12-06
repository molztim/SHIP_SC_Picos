import socket
import time
from micro_wlan import *
from machine import Pin, I2C

led = Pin("LED", Pin.OUT,value=1)

SSID = 'SHIP_PicoNet'
PASS = 'ThereIsAlwaysABiggerFish'

IP = ('10.42.0.100' ,'255.255.255.0','10.42.0.1','10.42.0.1')
wlan_ips = '0.0.0.0'
for i in range(5):
    try:
        wlan_ips = t_wlan(SSID,PASS,IP)
        print("Device IP:",wlan_ips[0],"\n")
        time.sleep_ms(1000)
        break
    except Exception as e:
        print(e)
        led.toggle()
        time.sleep_ms(100)
        led.toggle()
        led.off()
        raise RuntimeError 
    
if wlan_ips == "0.0.0.0":
    exit()
    
led.off()

#Start Server socket
addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
s = socket.socket()
s.bind(('',80))
s.listen(5)
print('listening on', addr)

while True:
    cl, addr = s.accept()
    while True:
        try:
            package = cl.recv(2**10)
            rcv = package.decode('utf-8')
            print("Received bytes: ",rcv)        
            response = "PING!"+IP[0]
            cl.send(response+'\r')
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            print("Close interaction with: {}\n".format(e))
            time.sleep(2)
            break
    




