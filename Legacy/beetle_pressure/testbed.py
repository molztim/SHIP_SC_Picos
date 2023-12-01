from machine import Pin,I2C,ADC
from readout import pressure_readout, level_readout
import time
# Initialisierung des ADC0 (GPIO26)
adc0 = ADC(0)

while True:
    press = pressure_readout(adc0)
    level = level_readout(adc0)
    print(press,level)
    time.sleep(1)

