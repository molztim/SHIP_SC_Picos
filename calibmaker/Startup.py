from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin,I2C,ADC
from eMUSIC_register import *
from I2C_CAEN import A7585
from eMUSIC import eMUSIC 

print("--- Startup ---")

enable_Pin = Pin(22, Pin.OUT, value=0)

DEV = A7585(112,4,5)
DEV.startup(80, 10, 43, 2,2)

utime.sleep_ms(10)

EMUSIC = eMUSIC(17,18,16,19)
eMUSIC_config = EMUSIC.read_calib()
EMUSIC.write_config(eMUSIC_config)

utime.sleep_ms(10)

enable_Pin.value(1)

print("--- Startup Finished! ---")