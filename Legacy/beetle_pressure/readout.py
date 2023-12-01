from machine import Pin,I2C,ADC
import utime as time
    
    
def pressure_readout(adc,ohm = 150,adc_offset = 310):
    
    low = 4 #mA
    high = 20 #mA
    v_low = low * ohm / 1000 #V
    v_high = high * ohm / 1000 #V
    
    adc_step = 3.3/(2**12) #ADC/V
    read0 = adc.read_u16()/16 - adc_offset/16
    measV = read0*adc_step
    pressure = ((measV / ohm * 1000) - low)/16 #bar
    return pressure #bar

def level_readout(adc,ohm = 150,adc_offset = 310):
    
    pressure = pressure_readout(adc,ohm=ohm,adc_offset=adc_offset)
    density = 863 #kg/m^3
    g = 9.81 #m/s^2
    level = pressure * 1e5 / (g*density)
    return level

#adc0 = ADC(0)

#while True:
#    press = pressure_readout(adc0)
#    level = level_readout(adc0)
#    print(press,level)
#    time.sleep(1)





