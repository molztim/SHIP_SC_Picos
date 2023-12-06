import _thread
import socket
from time import sleep
from micro_wlan import *
from machine import Pin, I2C
import os
from machine import RTC
rtc = RTC()

#The SSID and PW of the network. The IP in IP is unique for each device, but nor for eacht task
SSID = "SHIP_PicoNet"
PASS = "ThereIsAlwaysABiggerFish"
IP = ('10.42.0.100','255.255.255.0', '10.42.0.1', '10.42.0.1')

#At some point in time, I wrote my own WLAN lib with just a few simple commands. Its just handy.
wlan_ips = t_wlan(SSID,PASS,IP)
print("Device IP:",wlan_ips[0],"\n")
time.sleep_ms(100)

#Create the socket for other devices to connect to.

addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
s = socket.socket()
#Dunno how it does this, but this kills the socket on soft reset
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',80))
s.listen(5)
print('listening on', addr)

while True:
    #Look up if there is already a device to be used by scanning the internal file system.
    if 'device.py' not in os.listdir():
        cl, addr = s.accept()
        while True:
            try:
                #Receive the package as one
                package = cl.recv(10000)
                rcv = package.decode('utf-8')
                print("Received data: ",rcv[:25],"...")

                #Split the receive in file names and content by #-#
                parts = rcv.split("#-#")
                names = parts[1::2]
                content = parts[2::2]
                print("Names: ",names)

                #Create new files from file names and content
                for name, data in zip(names,content):
                    #pint(f"Name: {name} , {data}")
                    file = open(name, 'w')
                    file.write(data)
                    file.close()

                cl.send("Okay!")
                sleep(0.1)
                print('Datei wurde erfolgreich importiert')
                break
            except Exception as e:
                print(e)
                cl.close()
                s.close()
                break
    else:
        print("Found device!")
        break
    
global_data_variable = 0
global_command = ""
global_operation_flag = 0

print("Starting Device!")
import device 
#device.start(s,addr)
sensor = device.device(rtc,s,addr)

core2_process = _thread.start_new_thread(sensor.server(), ())

while True:
    cl, addr = s.accept()
    while True:
        try:
            #Get the data, decode it into UTF8 and print the command
            package = cl.recv(1024)
            rcv = package.decode('utf-8')
            print("Received data: ",rcv)

            #First, send the command to the 2nd core into the class sensor
            sensor.set_command(rcv)
            #Then send the sensor flag to True to trigger the data exchange
            sensor.set_flag(True)

            #Wait until the 2nd core says that the data is written
            while sensor.get_flag:
                pass
            
            #Afterwards get data from exchange and send data
            response = sensor.get_data()
            cl.send(str(response))
        except Exception as e:
            #Close socket (must have!)
            cl.close()
            print("Close interaction with: {}\n".format(e))
            time.sleep(2)
            break
