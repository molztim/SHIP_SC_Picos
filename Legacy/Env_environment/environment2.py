# Complete project details at https://RandomNerdTutorials.com
#https://randomnerdtutorials.com/micropython-bme280-esp32
from machine import Pin, I2C
from time import sleep
import bme280 as BME280

led = Pin("LED", Pin.OUT)
led.on()

# ESP32 - Pin assignment
i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c)

#Calibration
QNH = 1.22 #hPa pro 10m

height_garden = 277 #m NN
garden_height = 2#m over ground
height_roof = 323.5 #m NN
roof:height = 51.3 #m over ground
freiburg_height = 264 #m NN

sixfloor = 23.4 #m
heighterr = 3 #m
presserr = QNH * heighterr

comp = 1019.454 #hPa, 277m NN

from machine import RTC
rtc = RTC()

for i in range(24*4):

    now = rtc.datetime()

    
    
    head = "{:02d}:{:02d}:{:02d}".format(now[4],now[5],now[6])
    text = ""
    for j in range(1):
        data = bme.temperature
        text+= f"{data},"
    
    
    print('Pressure reading: ', text)    
    
    data = f"[{head}; {text[:-1]}],"

    f = open('test.txt','a')
    f.write(data)
    f.close()
    led.toggle()
    sleep(1)
    led.toggle()
    
    print(f"Finished Measurement {i}h - {head}\n")
    sleep(60*60 - 1)
    