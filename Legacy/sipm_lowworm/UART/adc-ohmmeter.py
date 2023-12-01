# Bibliotheken laden
from machine import ADC
from utime import sleep

# Initialisierung des ADC0 (GPIO26)
adc0 = ADC(0)

# Initialisierung des ADC1 (GPIO27)
adc1 = ADC(1)

#16 Bit words
bit = 2**16

# Wiederholung
while True:
    # ADC0 als Dezimalzahl lesen
    read0 = adc0.read_u16()/bit * 3.3
    read1 = adc1.read_u16()/bit * 3.3
    # Ausgabe in der Kommandozeile/Shell
    print('ADC0:', read0,"V")
    print('ADC1:', read1,"V")
    print()
    # Warten
    sleep(2)