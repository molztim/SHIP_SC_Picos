
#An examplary sensor/device
from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin,I2C,ADC
from eMUSIC_register import *
from I2C_CAEN import A7585
from eMUSIC import eMUSIC 


class device:

    def __init__(self,rtc):
        try:
            self.rtc = rtc          #The rtc
            self.ID = "SIPM & EMUSIC POWER 10.42.0.132"
            self.IP = '10.42.0.132'
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.data = 0           #Main data 
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel
            self.voltage = 43       
            self.max_voltage = 80.0
            self.max_current = 10
            self.ramp = 2
            self.TMP37 = [0,50,0] #C²/V, C/V, V
            self.enable_Pin = Pin(22, Pin.OUT, value=0)
            self.HVStatus = 0
            self.eMUSIC_config = []

            try:
                self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus  = config_reader()
            except:
                log("Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration")


            try:
                self.DEV = A7585(112,4,5)
                self.DEV.startup(self.max_voltage, self.max_current, self.voltage, self.ramp,rampuptime=self.ramp)
                self.DEV.SetTemperatureSensor("CUSTOM", *self.TMP37)
                #self.DEV.SetSIPMtcoef(-34)
            except Exception as e:
                log(f"A7585D cannot be started up with Error: {e}")
                error_log(f"A7585D cannot be started up with Error: {e}")
                raise RuntimeError(f"A7585D cannot be started up with Error: {e}")

            utime.sleep_ms(10)
            try:
                self.EMUSIC = eMUSIC(17,18,16,19)
                self.eMUSIC_config = self.EMUSIC.read_calib()
                self.EMUSIC.write_config(self.eMUSIC_config)
            except Exception as e:
                log(f"EMUSIC Controller object cannot be started up with Error: {e}")
                error_log(f"EMUSIC Controller object cannot be started up with Error: {e}")
                raise RuntimeError(f"EMUSIC Controller object cannot be started up with Error: {e}")


            log("Device Up!")
            utime.sleep_ms(10)
            self.enable_Pin.value(1)

        except:
            raise RuntimeError("Error 01: Init error")
        
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    
    def measurement(self):
        eMUSIC_flag = True
        while self.runFlag:
            if not self.read_flag:
                start = utime.ticks_ms()
                Vout = self.DEV.GetVout()
                Iout = self.DEV.GetIout()
                Vin = self.DEV.GetVin()
                statusHV = self.DEV.GetHVOn()
                connectionHV = self.DEV.GetConnectionStatus()
                #temp = (self.DEV.GetTref() - 32) * 5/9 
                temp = self.DEV.GetTref()

                if eMUSIC_flag:
                    self.eMUSIC_config = self.EMUSIC.read_config()
                    eMUSIC_flag = False
                else: 
                    eMUSIC_flag = True 

                saved_config = self.EMUSIC.read_calib()    
                config_status = int(self.eMUSIC_config==saved_config)
                if config_status == 0:
                    self.EMUSIC.write_config(saved_config)
                    log("Renewed Config!")

                ch_status = ",".join(str(x) for x in self.eMUSIC_config[24::11])
                pz_status = ",".join(str(x) for x in self.eMUSIC_config[29::11])
                rladpz_status = self.eMUSIC_config[17]
                capppz_status = self.eMUSIC_config[16]
                vdcch_status = self.eMUSIC_config[3]
                lowat_status = self.eMUSIC_config[0]
                offsset = ",".join(str(x) for x in self.eMUSIC_config[26::11]) 



                self.data = f"{Vout:.2f},{Iout:.2f},{Vin:.2f},{statusHV:.2f},{connectionHV:.2f},{config_status},{ch_status},{pz_status},{rladpz_status},{capppz_status},{vdcch_status},{lowat_status},{offsset},{temp:.2f}"       
                stop = utime.ticks_ms()

                #print(f"Data: {self.data} {utime.ticks_diff(stop,start)}")
                utime.sleep(30)
            

    def server(self,received):
        if "GET_EMUSIC_CONF" in received:
            self.read_flag = True
            current_config = self.EMUSIC.read_config()
            self.read_flag = False
            return f"{current_config}"
        
        elif "GET" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            answer = self.data
            self.read_flag = False

            #Now we gan return the data
            return answer
        
        elif "SET" in received:
            self.read_flag = True
            if "SET_V" in received:
                Vnew = float(received.split(" ")[1])
                self.DEV.SetV(Vnew)
            elif "SET_MAXV" in received:
                Vnew = float(received.split(" ")[1])
                self.DEV.SetMaxV(Vnew)
            elif "SET_MAXI" in received:
                Inew = float(received.split(" ")[1])
                self.DEV.SetMaxI(Inew)
            elif "SET_RAMP" in received:
                Rampnew = float(received.split(" ")[1])
                self.DEV.SetRampVs(Rampnew)
            elif "SET_MODE" in received:
                Modenew = int(received.split(" ")[1])
                self.DEV.SetMode(Modenew)
            elif "SET_ENA" in received:
                ENA = int(received.split(" ")[1])
                self.enable_Pin.value(ENA)
                self.HVStatus = ENA

            elif "SET_CHENABLE" in received:
                ENA = int(received.split(" ")[1])
                CHA = int(received.split(" ")[0][-1])-1
                self.EMUSIC.write_eMUSIC(ENA,"ENCH",channel = CHA)
                self.EMUSIC.write_line(ENA,"ENCH",channel = CHA)
                
            elif "SET_CHPZ" in received:
                ENA = int(received.split(" ")[1])
                CHA = int(received.split(" ")[0][-1])-1
                self.EMUSIC.write_eMUSIC(ENA,"ENPZ",channel = CHA)
                
            elif "SET_CHOFFSET" in received:
                ENA = int(received.split(" ")[1])
                CHA = int(received.split(" ")[0][-1])-1
                self.EMUSIC.write_eMUSIC(ENA,"DVOFFSET",channel = CHA)
                
            elif "SET_LOWAT" in received:
                ENA = int(received.split(" ")[1])
                self.EMUSIC.write_eMUSIC(ENA,"LOWATLAD_PZ")
                
            elif "SET_VDCCH" in received:
                ENA = int(received.split(" ")[1])
                self.EMUSIC.write_eMUSIC(ENA,"VDCCH")
                
            elif "SET_CAPPPZ" in received:
                ENA = int(received.split(" ")[1])
                self.EMUSIC.write_eMUSIC(ENA,"CAPPZ")
                
            elif "SET_RLADPZ" in received:
                ENA = int(received.split(" ")[1])
                self.EMUSIC.write_eMUSIC(ENA,"RLAD")
            
            elif "SET_eMUSIC" in received:
                data = received
                config = [int(x) for x in data.split(" ",1)[1].replace(" ","")[1:-1].split(",")]
                log("Config rcv.! :",config[:5],"...")
                self.EMUSIC.write_calib(config)
                self.EMUSIC.write_config(config)
                
            self.read_flag = False
            config_writer(self.rtc,[self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus])
            return "INTERNAL"
        else:
            return "A"
        
    def kill(self):
        self.runFlag = False
        gc.collect()
        _thread.exit()
