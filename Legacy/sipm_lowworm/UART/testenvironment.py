# Bibliotheken laden
from machine import UART, Pin
from utime import sleep

"""
# UART0 initialisieren
uart0 = UART(0, baudrate = 115200, tx=Pin(0), rx=Pin(1))
print('UART0:', uart0)
print()
"""

# UART1 initialisieren
uart1 = UART(1, baudrate = 57600, tx=Pin(8), rx=Pin(9)) #57600, 76800
print('UART1:', uart1)
print()


#Daten zum Senden
if False:
    txData = b'\xc0\xe4\x90'
    #print(int("0xc0",16),int("0xe4",16),int("0x90",16))
    print('Daten senden:', txData)

    # Daten senden
    uart1.write(txData)


# Daten empfangen und ausgeben
buffer = []
memory = None


print("Ready!")
while True:
    try:
        rxData = uart1.readline()
        if rxData != None or memory != None:
            #char = rxData.decode('utf-8')
            #buffer += char
            
            #integer = int("0"+str(rxData)[3:-1],16)
            #print("Char:",char,"Data:",rxData)
            

            #integer = int("0"+str(rxData)[3:-1],16)
            #print(rxData, "Number: ",integer)
            print(rxData)
            
            if rxData == None and memory != None:
                print("#####################################################")
                
            memory = rxData

            """
            if char == "\r":
                #print(''.join(buffer))
                #buffer = []

            else:
                None
            """
    except:
        None

