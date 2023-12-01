# Bibliotheken laden
from machine import Pin, I2C
import time

# Initialisierung I2C-Pins
i2c_sda = Pin(0)
i2c_scl = Pin(1)
xshut = Pin(15,Pin.OUT,value=1)

# Initialisierung I2C
i2c = I2C(0,sda=i2c_sda,scl=i2c_scl,freq=200000)

time.sleep(1)
# I2C-Bus-Scan
xshut.off()
print('Scan I2C Bus...')
devices = i2c.scan()
"""
index = bytearray(2)
print(index)
try:
    #data = i2c.readfrom_mem(0x029,0x00, 1, addrsize=16)
    acks=i2c.writeto(0x29,index)
    print(acks)
    #data = i2c.readfrom(0x29,1)
    print("Yes!",data)
except Exception as e:
    print("Nope...",e)
"""
 #Scanergebnis ausgeben
if len(devices) == 0:
    print('Kein I2C-Gerät gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))