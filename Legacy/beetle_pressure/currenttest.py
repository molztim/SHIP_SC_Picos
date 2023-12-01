from machine import Pin, I2C
import ina219
import utime
 
i = I2C(0, scl=Pin(1), sda=Pin(0))
utime.sleep_ms(100)
print("I2C Bus Scan: ", i.scan(), "\n")

utime.sleep_ms(100)
 
sensor = ina219.INA219(i)
sensor.set_calibration_16V_6A()
 
r_s = 0.03333  # shunt resistor on INA219 board
 
# current is returned in milliamps
while True:
    print("Current       / mA: %8.3f" % (sensor.current))
    # shunt_voltage is returned in volts
    print("Shunt voltage / mV: %8.3f" % (sensor.shunt_voltage * 1000))
    # estimate supply voltage from known resistance * sensed current+
    utime.sleep(2)
    #print("NEU")
