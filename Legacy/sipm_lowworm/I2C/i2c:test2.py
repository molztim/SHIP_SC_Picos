# Bibliotheken laden
from machine import Pin, I2C
import struct

#from I2C.i2c_caen import A7585

# Initialisierung I2C
addr = 112
i2c_sda = Pin(20)
i2c_scl = Pin(21)
i2c = I2C(0,sda=i2c_sda,scl=i2c_scl,freq=100000)


#Messages als bytes



n = 0.1015625
buffer = struct.pack("f",n)
print(buffer.hex())

a = b'\x00\x00\xd0='
print(struct.unpack("f",a))

b = b"\x00\x00\xd0\x3d"
print(struct.unpack("f",b))

#print(struct.unpack("<f",buffer))



#print("Message:",buffer)
#original = struct.unpack("B",buffer)
#print(original)
#ack1 = i2c.writeto(addr,buffer)
#print(ack1)

