import network
import socket
import binascii
import ubinascii

import machine
import utime as time
led = machine.Pin('LED', machine.Pin.OUT, value=1)
time.sleep(1)
led.toggle()
time.sleep(1)
led.toggle()
print("System up...")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

nets = wlan.scan()
if len(nets) > 0: print("Found some nets! Amount:",len(nets))
else: print("Nothing Found!")

for i in range(len(nets)):
    outstr = ""
    outstr += "SSID: "+str(nets[i][0].decode('ascii'))
    outstr += " BSSID: "+str(binascii.hexlify(nets[i][1]))
    outstr += " Channel: "+str(nets[i][2])
    outstr += " RSSI: "+str(nets[i][3])
    outstr += " Sec.: "+str(nets[i][4])
    outstr += " Hidden=: "+str(nets[i][5])
    print(outstr)