#Bibliotheken laden
from machine import Pin, I2C
import struct
import utime as time

NIPMREG_HVSTATUS = 0 
NIPMREG_FBMODE = 1
NIPMREG_VTARGET = 2
NIPMREG_RAMP = 3
NIPMREG_MAXV =4
NIPMREG_MAXI =5
NIPMREG_MAXT = 6
NIPMREG_TEMP_M2 = 7
NIPMREG_TEMP_M = 8
NIPMREG_TEMP_Q = 9
NIPMREG_ALFA_V = 10
NIPMREG_ALFA_I = 11
NIPMREG_ALFA_VREF = 12
NIPMREG_ALFA_TREF =13
NIPMREG_TCOEF =28
NIPMREG_LUTENABLE = 29
NIPMREG_PIDENABLE = 30
NIPMREG_EMERGENCYSTOP = 31
NIPMREG_IZERO =33
NIPMREG_LUTADDRESS = 36
NIPMREG_LUTT = 37
NIPMREG_LUTV = 38
NIPMREG_POINTn = 39
NIPMREG_IIC_BA = 40

NIPMREG_UNDERVOLTAGE = 227
NIPMREG_NTCTEMP = 228
NIPMREG_DIGITALIO = 229
NIPMREG_VIN = 230
NIPMREG_VOUT = 231
NIPMREG_IOUT = 232
NIPMREG_VREF = 233
NIPMREG_TREF = 234
NIPMREG_VTARGetR = 235
NIPMREG_RTARGetR = 236
NIPMREG_CORRECTIONVOLTAGE = 237
NIPMREG_PIDOUT = 238
NIPMREG_COMPV = 249
NIPMREG_COMPI = 250

NIPMREG_PDCODE = 251
NIPMREG_FWVER = 252
NIPMREG_HWVER = 253
NIPMREG_SN = 254
NIPMREG_WEEPROM = 255

class A7585:
    
    def __init__(self, address,SDA,SCL):
        self.address = address
        self.ramp = 0
        self.maxV = 0
        
        i2c_sda = Pin(SDA) 
        i2c_scl = Pin(SCL) 
        
        #i2c_sda = Pin(20) 
        #i2c_scl = Pin(21) 
        try:
            self.i2c = I2C(0,sda=i2c_sda,scl=i2c_scl,freq=100000)
        except:
            print("Error 01: Init error")
        
    def test_fun(self):
        buffer = struct.pack("B", 11)
        print("Message:",buffer)
        ack1 = self.i2c.writeto(self.address,buffer)
        print(ack1)
    
    #The functions that handle communication
    def SetNIPMRegFloat(self, register_n, float_data):
        bin_data = struct.pack("f",float_data)
        
        bin_type = struct.pack("B",3)
        bin_register = struct.pack("B",register_n)
        
        buffer = bin_register + bin_type + bin_data
        self.i2c.writeto(self.address, buffer)
        
    
    def SetNIPMRegBoolean(self, register_n, bool_data):
        bool_data = int(bool_data==True)
        bin_data = struct.pack("B",bool_data)
        
        bin_register = struct.pack("B",register_n)
        bin_type = struct.pack("B",2)
        
        buffer = bin_register + bin_type + bin_data
        self.i2c.writeto(self.address, buffer)
        
    
    def SetNIPMRegInteger(self, register_n, int_data):
        bin_data = int_data.to_bytes(4,"little")
        
        bin_register = struct.pack("B",register_n)
        bin_type = struct.pack("B",0)
        
        buffer = bin_register + bin_type + bin_data
        self.i2c.writeto(self.address, buffer)
        
    
    def GetNIPMRegFloat(self, register_n):
        bin_register = struct.pack("B",register_n)
        bin_type = struct.pack("B",3)     
        bin_memory_addr = bin_register + bin_type
        
        self.i2c.writeto(self.address,bin_memory_addr,False)
        buffer = self.i2c.readfrom(self.address,4,True)

        float_data = struct.unpack("f",buffer)
        return float_data[0]
    
    def GetNIPMRegBoolean(self, register_n):
        bin_register = struct.pack("B",register_n)        
        bin_type = struct.pack("B",2)
        bin_memory_addr = bin_register + bin_type
        
        self.i2c.writeto(self.address,bin_memory_addr,False)
        buffer = self.i2c.readfrom(self.address,4,True)
        
        bool_data = struct.unpack("i",buffer)
        return (bool_data[0]==1)
    
    def GetNIPMRegInteger(self, register_n):
        bin_register = struct.pack("B",register_n)        
        bin_type = struct.pack("B",0)
        bin_memory_addr = bin_register + bin_type
        
        self.i2c.writeto(self.address,bin_memory_addr,False)
        buffer = self.i2c.readfrom(self.address,4,True)
        
        int_data = struct.unpack("i",buffer)
        
        return int_data[0]
    
     #High Level Commands
    
    def SetV(self, v):
        self.SetNIPMRegFloat(NIPMREG_VTARGET, v)
    
    def SetMaxV(self, v):
        self.maxV = v
        self.SetNIPMRegFloat(NIPMREG_MAXV, v)
    
    def SetMaxI(self, i):
        self.SetNIPMRegFloat(NIPMREG_MAXI, i)
    
    def SetEnable(self, on):
        self.SetNIPMRegBoolean(NIPMREG_HVSTATUS,on)
    
    def SetRampVs(self, vs):
        self.ramp = vs
        self.SetNIPMRegFloat(NIPMREG_RAMP, vs)
    
    def SetMode(self, m):
        self.SetNIPMRegInteger(NIPMREG_FBMODE, m)
        
    def SetTemperatureSensor(self,SensorModel, term_m2, term_m, term_q ):
        #The function: Takes in voltage, returns temperature
        # Temp = term_m2*x^2 + term_m*x + term_q  x = voltage
        
        
        if SensorModel == "TMP100":
            self.SetNIPMRegFloat(NIPMREG_TEMP_M2, 0)
            self.SetNIPMRegFloat(NIPMREG_TEMP_M, 50)
            self.SetNIPMRegFloat(NIPMREG_TEMP_Q, 0)
        if SensorModel ==" LM94021":
            self.SetNIPMRegFloat(NIPMREG_TEMP_M2, 0)
            self.SetNIPMRegFloat(NIPMREG_TEMP_M, -73.53)
            self.SetNIPMRegFloat(NIPMREG_TEMP_Q, 193.9)
        if SensorModel == "CUSTOM":
            self.SetNIPMRegFloat(NIPMREG_TEMP_M2, term_m2)
            self.SetNIPMRegFloat(NIPMREG_TEMP_M, term_m)
            self.SetNIPMRegFloat(NIPMREG_TEMP_Q, term_q)
            
    def SetSIPMtcoef(self,tcomp):
        #tcomp is the thermal coefficient compensation in mV/°C (typical: -34 mV/°C)
        self.SetNIPMRegFloat(NIPMREG_TCOEF, tcomp)
        

    #Getters
    
    def GetMode(self):
        m = self.GetNIPMRegInteger(NIPMREG_FBMODE)
        return m

    def GetVin(self):
        v = self.GetNIPMRegFloat(NIPMREG_VIN)
        return v
    
    def GetVout(self):
        v = self.GetNIPMRegFloat(NIPMREG_VOUT)
        return v
    
    def GetIout(self):
        i = self.GetNIPMRegFloat(NIPMREG_IOUT)
        return i
    
    def GetHVOn(self):
        b = self.GetNIPMRegBoolean(NIPMREG_HVSTATUS)
        return b
    
    def GetConnectionStatus(self):
        pd = self.GetNIPMRegInteger(NIPMREG_PDCODE)
        if (pd==50 or pd == 51 or pd == 52 or pd == 53 or pd == 54 or pd ==55 or pd == 56 or pd == 1):
            return True
        else:
            return False
        
    def GetTref(self):
        t = self.GetNIPMRegFloat(NIPMREG_TREF)
        return t
    
    def GetVcorrection(self):
        v = self.GetNIPMRegFloat(NIPMREG_CORRECTIONVOLTAGE)
        return v
    
    def GetRampVs(self):
        return self.ramp
    
    def GetMaxV(self):
        return self.maxV
    

    def startup(self,MaxV,MaxI,SetV,Ramp,Mode=0,intervall=100,rampuptime=15):
        self.SetMode(Mode)
        time.sleep_ms(intervall)

        self.SetMaxV(MaxV)
        time.sleep_ms(intervall)

        self.SetMaxI(MaxI)
        time.sleep_ms(intervall)

        self.SetV(SetV)
        time.sleep_ms(intervall)

        self.SetRampVs(Ramp)
        time.sleep_ms(intervall)

        print("I2C parameters transmitted, wait for spooling up ({}sec.)...".format(rampuptime))
        time.sleep(rampuptime)
        
        #self.SetEnable(True)
        return True

    
    
    
    
    

