# Bibliotheken laden
import machine
import network 
import utime as time
import binascii
import ubinascii

from eMUSIC_registers import *

from machine import SPI, Pin

CSN = 17
cs = Pin(CSN, mode=Pin.OUT, value=1)
spi = SPI(0, baudrate=1000000, polarity=0, phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(18),mosi=Pin(19),miso=Pin(16)) #Mode 1 connection #1000000

class eMUSIC:
    
    def __init__(self, CSN, SCK, MISO, MOSI):
        csn = Pin(CSN) #17
        sck = Pin(SCK) #18
        miso = Pin(MISO) #16
        mosi = Pin(MOSI) #19
        
        self.spi = SPI(0, baudrate=1000000, polarity=0, phase=1,bits=8,firstbit=SPI.MSB,sck=sck,mosi=mosi,miso=miso) #Mode 1 connection #1000000
        self.cs = csn
        
        
    def spi_write(self,reg,data):
        msg = bytearray()
        msg.append(reg)
        msg+=data
        try:
            self.cs.value(0)
            self.spi.write(msg)
            self.cs.value(1)
        except:
            print("Error 21: Error in writing via SPI. Check comm.")
    
    def spi_read(self,reg,nbytes=2):           
        msg = bytearray()
        msg.append(reg+128)
        try:
            
            self.cs.value(0)
            self.spi.write(msg)
            data = self.spi.read(nbytes)
            self.cs.value(1)
            
            return data
        
        except Exception as e:
            print("Error 20: Could not read data ia SPI. Check SPI!")
            print("{0} : {1}".format(type(ex).__name__, ex.args))
            return None

    def read_eMUSIC(self,registername, channel = 0, debug=False):
        data = None
        register = eMUSIC_register[registername][0][channel]
        bits = eMUSIC_register[registername][1]
        
        data = self.spi_read(register)
        
        if debug:
            print("READ COMMAND")
            print("Register to be called:",register,", Position(s) in return:",bits)
            bit_data = ' '.join(f'{x:08b}' for x in data)
            print(f"Read Data: {data} {bit_data}\n")
        return data
    
    def write_eMUSIC(self, data,registername,channel=0, debug=False):
        register = eMUSIC_register[registername][0][channel]
        bits = eMUSIC_register[registername][1]
        
        prev = self.read_eMUSIC(registername, channel = channel, debug=debug)
        bit_prev = ''.join(f'{x:08b}' for x in prev)
        
        data = bytes([data])
        bit_data = ''.join(f'{x:b}' for x in data)
        bit_data = '0' * (len(bits) - len(bit_data)) + bit_data
        
        new_bits = bit_prev[:bits[0]] + bit_data + bit_prev[bits[-1]+1:]
        write_data = int(new_bits,2).to_bytes(2,'big')

        if debug:
            print("WRITE COMMAND")
            print(f"Bits in bitprev: {bit_prev}")
            print("Reigster to be called:",register,", Position(s) in return:",bits)
            print(f"Outgoing Data: {write_data} - {data} {bit_data} \n")
        
        self.spi_write(register,write_data)
        return None

    def read_config(self, debug=False):
        red_config = []
        channel = 0
        for key in CONFIG_KEY_LIST:
            if key == "FASTOR":
                red_config.append(0)
                continue
            data = self.read_eMUSIC(key, channel = channel,debug = debug)
            pos = eMUSIC_register[key][1]        
            bit_data = ''.join(f'{x:08b}' for x in data)
            bits = ''.join([bit_data[i] for i in pos])
            red_config.append(int(bits,2))
            if key == "PENZPZCOMP":
                channel +=1

        return red_config

    def write_config(self, pck,debug=False):
        channel = 0
        for i in range(len(pck)):
            data = pck[i]
            register = CONFIG_KEY_LIST[i]
            
            if register == "FASTOR": continue
            try:
                self.write_eMUSIC(data, register, channel = channel, debug =debug)
                if register == "PENZPZCOMP":
                    channel +=1
                #returned = read_eMUSIC(register, channel = channel, debug =debug)
                #print(f"Register: {register} {channel} ok, data {data} send.\nReturned Data {returned}")
            except Exception as e:
                print(f"Exception found at: Register: {register} {channel} {data} - {e}")

        return None
    
    
    def write_line(self,data,regi,channel=0):
        pos = eMUSIC_configfile[regi][channel]
        file = open('calib.txt', 'r').read()
        text = list(map(int, file.split(", ")))
        text[pos] = data
        text = ", ".join(f'{x}' for x in text)
        file = open('calib.txt', 'w')
        file.write(text)
        file.close()
        return None
    
    def read_calib(self):
        file = open('calib.txt', 'r').read()
        data = list(map(int, file.split(", ")))
        return data
    
    def write_calib(self,data):
        file = open('calib.txt', 'w')
        text = ", ".join(f'{x}' for x in data)
        file.write(text)
        file.close()
        return None
        
#eprom = [1, 144, 144, 129, 111, 7, 4, 6, 30, 1, 1, 0, 1, 255, 38, 12, 5, 48, 3, 4, 6, 17, 3, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1, 1, 0, 255, 1, 1, 1, 1, 120, 1, 1, 1]
#write_config(EMUSIC_CONFIG)
#configile = read_config()
#read_eMUSIC('VCM', debug=True)


