#Ports
I2C_SDA = 4
I2C_SCL = 5
I2C_ENA = 22
from machine import Pin, I2C

from I2C.i2c_caen import A7585

# Pin Init
enable_Pin = Pin(I2C_ENA, Pin.OUT, value=0)
print("System up...")

#I2C Init
DEV = A7585(112,I2C_SDA,I2C_SCL)
DEV.startup(80,10,30,2,rampuptime=2)
enable_Pin.value(1)
print("I2C ready!")
# Listen for connections
Vrmp = DEV.GetRampVs()
print(Vrmp)

 




