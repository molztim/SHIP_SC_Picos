from machine import Pin, I2C
from vl53l1x import VL53L1X
import time
sda = Pin(4)
scl = Pin(5)
xshut = Pin(6,Pin.OUT,value=1)
id = 0
print("Setting up i2c bus ", id)

i2c = I2C(id=id, sda=sda, scl=scl)

print(repr(i2c.scan()))
if 0x29 not in i2c.scan():
    print("Failed to find device")
    raise RuntimeError()

distance = VL53L1X(i2c)
while True:
    print("range: mm ", distance.read())
    time.sleep_ms(50)