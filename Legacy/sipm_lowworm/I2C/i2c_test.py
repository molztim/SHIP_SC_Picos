# Bibliotheken laden
from machine import Pin, I2C
import utime as time

# Initialisierung I2C-Pins
i2c_sda = Pin(4)
i2c_scl = Pin(5)

# Initialisierung I2C
i2c = I2C(0,sda=i2c_sda,scl=i2c_scl,freq=100000)

# I2C-Bus-Scan
print('Scan I2C Bus...')
devices = i2c.scan()

# Scanergebnis ausgeben
if len(devices) == 0:
    print('Kein I2C-Gerät gefunden!')
    time.sleep(1.2)
    led.toggle()
    time.sleep(1.2)
    led.toggle()
else:
    print('I2C-Geräte gefunden:', len(devices))
    time.sleep(5)
    led.toggle()
    time.sleep(5)
    led.toggle()
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))