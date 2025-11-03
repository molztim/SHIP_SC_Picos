# Version 3.0 For TB Fall 2025
# Now Includes FastIC+
from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin,I2C,ADC
from eMUSIC_register import *
from I2C_CAEN import A7585
from eMUSIC import eMUSIC
from FastIC_plus import FastIC, fastic_registers, alpha_keylist

# The main class for the SIPM power & Control devices.
# It contains just this class device to call when starting the sensor operation.
# MEASUREMENT then runs the data takeing from the physical devices at core #2
# SERVER handles the communication to Doberman at core #1

class device:

    def __init__(self,rtc):
        try:
            # Initialize all the variables we need for operation
            self.rtc = rtc          #The rtc
            self.ID = "SIPM & EMUSIC POWER 10.42.0.125"
            self.IP = '10.42.0.125'
            
            

            self.read_flag = False  #Blocks/releases the data varaible for reading
            self.data = 0           #Main data
            self.runFlag = True     #Activate while loop for meausrements, important to to shut down the kernel
            self.voltage = 43       # CAEN Parameters
            self.max_voltage = 50.0
            self.max_current = 10
            self.ramp = 2
            self.TMP37 = [0,50,0] #C²/V, C/V, V
            self.enable_Pin = Pin(22, Pin.OUT, value=0)
            self.HVStatus = 0
            self.Mode = 2
            self.config_status = 1 # Config status: Is config on chip = local calib?
            
            self.device_type = 0 # 0 = EMUSIC, 1 = FASTIC+ to determine which device we have
            self.eMUSIC_config = []
            self.FastIC_config = []
            self.configID = 1000 # This ID is the ID of the config document which we use for the FastIC configuration 
            
            try:
                # We have a seperate file to keep all the CAEN PS properties stored and need to laod the last one here.
                self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus,self.Mode,self.configID,self.device_type = config_reader()
                self.Mode = int((self.Mode!=0))*2
            except Exception as e:
                log(f"Error loading calibration file: Could not transfer data from list of calibrations to variables in class. Continue with normal configuration - {e}")
            
            try:
                # Initialize the CAEN PS, set the HV parameters, the temperature sensor and how we want to run the temperture compensation
                self.DEV = A7585(112,4,5)
                self.DEV.startup(self.max_voltage, self.max_current, self.voltage, self.ramp,Mode=self.Mode,rampuptime=self.ramp)
                self.DEV.SetTemperatureSensor("CUSTOM", *self.TMP37)
                self.DEV.SetSIPMtcoef(-34)
            except Exception as e:
                log(f"A7585D cannot be started up with Error: {e}")
                error_log(f"A7585D cannot be started up with Error: {e}")
                #raise RuntimeError(f"A7585D cannot be started up with Error: {e}")

            utime.sleep_ms(10)
            # Here we start with initialising the EMUSIC / FastIC+
            # We create objects, read the local config, send them and then read back once to check if the transmission was correct
            if(self.device_type==0):
                try:
                    log("Start eMUSIC Controller Software")
                    rst_Pin = Pin(26, Pin.OUT, value=0)
                    self.EMUSIC = eMUSIC(17,18,16,19)
                    self.EMUSIC.write_config(self.EMUSIC.read_calib())
                    self.eMUSIC_config = self.EMUSIC.read_config()
                    saved_config = self.EMUSIC.read_calib()
                    config_status =  int(self.eMUSIC_config==saved_config)
                except Exception as e:
                    log(f"EMUSIC Controller object cannot be started up with Error: {e}")
                    error_log(f"EMUSIC Controller object cannot be started up with Error: {e}")
                    raise RuntimeError(f"EMUSIC Controller object cannot be started up with Error: {e}")
            
            else:
                try:
                    log("Start FASTIC+ Controller Software")
                    self.FastIC = FastIC(0x10,26,27)
                    saved_config = self.FastIC.read_calib()
                    self.FastIC.write_config(saved_config)
                    self.FastIC_config = self.FastIC.read_config()
                    config_status =  int(self.FastIC_config==saved_config)
                    #print("CONFIG STATUS: ",config_status)
                except:
                    log(f"FastIC+ Controller object cannot be started up with Error: {e}")
                    error_log(f"FastIC+ Controller object cannot be started up with Error: {e}")
                    raise RuntimeError(f"FastIC+ Controller object cannot be started up with Error: {e}")
               
            log("Device Up!")
            utime.sleep_ms(10)
            self.enable_Pin.value(1)

        except Exception as e:
            raise RuntimeError(f"Error 01: Init error - {e}")
    
    # Two getter that are hadny for debugging
    def getIP(self):
        return self.IP
    
    def getID(self):
        return self.ID
            
    # measurement is executed in the 2nd core every know and then.
    # In principle it reads out all the perihpery devices and saves the gathere data in self.data
    # This is differnet for the eMUSIC and FastIC+. Here we just send back the saved registers from
    # self.eMUSIC_config or seld. FastIC_config., because the transmissions interfere with the analog
    # waveforms.
    # There is also this runFlag. This runFlag is set by Core #1 (communication core) and manages when
    # which core can access the data in self.data. Quite important since we use multi processing!
    def measurement(self):
        #eMUSIC_flag = True
        while self.runFlag:
            if not self.read_flag:
                start = utime.ticks_ms()
                
                # Get data from the CAEN
                Vout = self.DEV.GetVout()
                Iout = self.DEV.GetIout()
                Vin = self.DEV.GetVin()
                statusHV = self.DEV.GetHVOn()
                connectionHV = self.DEV.GetConnectionStatus()
                #temp = (self.DEV.GetTref() - 32) * 5/9 
                mode = int(self.DEV.GetMode() == 2)
                temp = self.DEV.GetTref()
                
                vcorr = self.DEV.GetVcorrection() / 1000
                vref = self.DEV.GetVRef()
                vtarget = vref - vcorr
                
                #print(f"Measured Voltage: {Vout}")
                #print(vcorr,vref,vtarget,self.DEV.GetMode(),temp)
               
                # Here, we ask the EMUSIC/FASTIC+ for its configuration and prepare it for sending
                # ATM I found it more conveneint to just as some registers, not all.
                # There is an extra command ask for the entire configuration
                # The key here is: We only read the config at the beginning, and when we change the config.
                # The point is to minimize communication and duty on teh chip. The eMUSIC was most likely
                # Prone to such issues
                
                if (self.device_type == 0):
                    ch_status = ",".join(str(x) for x in self.eMUSIC_config[24+4::11])
                    pz_status = ",".join(str(x) for x in self.eMUSIC_config[29+4::11])
                    rladpz_status = self.eMUSIC_config[17+4]
                    capppz_status = self.eMUSIC_config[16+4]
                    vdcch_status = self.eMUSIC_config[3]
                    lowat_status = self.eMUSIC_config[0]
                    offsset = ",".join(str(x) for x in self.eMUSIC_config[26+4::11])
                    
                    dvth = ",".join(str(x) for x in self.eMUSIC_config[31+4::11])
                    #dvth = self.eMUSIC_config[31+4]
                    
                    # Test all channels for digital use
                    
                    #changeAllCH("PENCOMPSW",1) # Comperatore Enable
                    #changeAllCH("PENZPZCOMP",0) # Comperatore PZ
                    #changeAllCH("PHLCOMP",1) # Comperator Gain
                    #changeAllCH("ENDRVSE",0) # SE Driver Enable
                    PENCOMPSW = self.eMUSIC_config[33+4::11] == [1]*8
                    PENZPZCOMP = self.eMUSIC_config[34+4::11] == [0]*8
                    PHLCOMP = self.eMUSIC_config[32+4::11] == [1]*8
                    ENDRVSE = self.eMUSIC_config[30+4::11] == [0]*8

                    DIGIALL = int(all([PENCOMPSW,PENZPZCOMP,PHLCOMP,ENDRVSE]))
                    
                    SUMs = [int(self.eMUSIC_config[14+4] & 2**i != 0) for i in range(8)]               
                    #The order here must be CH0 -> CH7
                    sum_string = ",".join(str(x) for x in SUMs)
                    
                    ENPZHG = self.eMUSIC_config[13]
                    ENPZLG = self.eMUSIC_config[17]
                    HLSUMHG = self.eMUSIC_config[10]
                    HLSUMLG = self.eMUSIC_config[14]
                    ENBYPASSHG = self.eMUSIC_config[12]
                    ENBYPASSLG = self.eMUSIC_config[16] 
                    ENDIFFDRVHG = self.eMUSIC_config[11]
                    ENDIFFDRVLG = self.eMUSIC_config[15]
                    
                    self.data = f"{Vout:.3f},{Iout:.2f},{Vin:.2f},{statusHV:.2f},{connectionHV:.2f},{self.config_status},{ch_status},{pz_status},{rladpz_status},{capppz_status},{vdcch_status},{lowat_status},{offsset},{temp:.2f},{mode},{dvth},{DIGIALL},{sum_string},{ENPZHG},{ENPZLG},{HLSUMHG},{HLSUMLG},{ENBYPASSHG},{ENBYPASSLG},{ENDIFFDRVHG},{ENDIFFDRVLG},{vtarget:.3f},{self.device_type}"       
                else:
                    # Here we test, if we can chuck the entire config in one go
                    self.config_status = int(self.FastIC.read_calib()==self.FastIC.read_config())
                    hexconfig = "STR:"+"".join(f"{e:02X}" for e in self.FastIC_config)
                    self.data = f"{Vout:.3f},{Iout:.2f},{Vin:.2f},{statusHV:.2f},{connectionHV:.2f},{temp:.2f},{mode},{vtarget:.3f},{self.config_status},{self.configID},{self.device_type}"#  +  fastic_string
                    #print(f"Config Status: {self.config_status}")
                    
                stop = utime.ticks_ms()
                              
                #print(f"Data: {self.data} {utime.ticks_diff(stop,start)}")
                utime.sleep(5)
            
    # Server is the function we run on core #1
    # This handles the communication: WHich incomming command prompts which data transfer or action
    # I seperated the commands in "Get" and "Set".
    # GET has only 3 options: Get the full config of EMUSIC or FASTIC or just get what is supposed be the data.
    # SET has a mlutitude of options: One for each sensor parameter (like CAEN HV)
    # and one to set an entire, complete config for EMUSIC and FASTIC.
    # Why not makeing differnet sets for each register?
    # EMUSIC has 60 register, FASTIC has >300 registers. Its not worth the time.
    # Finally this one returns "INTERNAL" if it was a SET
    # or data if we had a GET
    def server(self,received):
        if "GET_EMUSIC_CONF" in received:
            #The readFlag inhiibts the writing of data to send the latest data back to teh main software
            self.read_flag = True
            current_config = self.EMUSIC.read_config()
            self.read_flag = False
            return f"{current_config}"
        
        elif "GET_FASTIC_CONF" in received:
            self.read_flag = True
            current_config = self.FastIC.read_config()
            self.read_flag = False
            hex_mess = "".join(f"{e:02X}" for e in current_config)
            return f"{hex_mess}"
        
        elif "GET" in received:
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
                self.voltage = Vnew
                
            elif "SET_MAXV" in received:
                Vnew = float(received.split(" ")[1])
                self.DEV.SetMaxV(Vnew)
                self.max_voltage = Vnew
                
            elif "SET_MAXI" in received:
                Inew = float(received.split(" ")[1])
                self.DEV.SetMaxI(Inew)
                self.max_current = Inew
                
            elif "SET_RAMP" in received:
                Rampnew = float(received.split(" ")[1])
                self.DEV.SetRampVs(Rampnew)
                self.ramp = Rampnew
                
            elif "SET_ENA" in received:
                ENA = int(received.split(" ")[1])
                self.enable_Pin.value(ENA)
                self.HVStatus = ENA
                
            elif "SET_MODE" in received:
                MODE = int(received.split(" ")[1])
                if MODE == 0:
                    self.DEV.SetMode(0) #Mode 0 is for digital mode w/ temp comp.
                    self.Mode = 0
                else:
                    self.DEV.SetMode(2) #Mode 2 is for digital mode with temp. comp
                    self.Mode = 2
                    
            elif "SET_DEVICE" in received:
                device = int(received.split(" ")[1]) # 0 = EMUSIC, 1 = FASTIC
                config_writer(self.rtc,[self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus,self.Mode,self.configID,device])
                return "INTERNAL"

                
            # Functions to receive, decode and set configurations
            
            elif "SET_EMUSIC_CONFIG" in received:
                data = received
                config = [int(x) for x in data.split(" ",1)[1].replace(" ","")[1:-1].split(",")]
                log("Config rcv.! :",config[:5],"...")
                self.EMUSIC.write_calib(config)
                self.EMUSIC.write_config(config)
                
                self.eMUSIC_config = self.EMUSIC.read_config()
                saved_config = self.EMUSIC.read_calib()
                self.config_status =  int(self.eMUSIC_config==saved_config)

            
            elif "SET_EMUSIC_DEBUG" in received:
                data = received
                config = [int(x) for x in data.split(" ",1)[1].replace(" ","")[1:-1].split(",")]
                log("Config rcv.! :",config[:5],"...")
                self.EMUSIC.write_calib(config)
                self.EMUSIC.write_config(config)
                
                utime.sleep_ms(100)
                                
                self.eMUSIC_config = self.EMUSIC.read_config()
                saved_config = self.EMUSIC.read_calib()
                self.config_status =  int(self.eMUSIC_config==saved_config)
                
                self.read_flag = False
                config_writer(self.rtc,[self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus,self.Mode,self.configID,self.device_type])
                
                return f"{self.eMUSIC_config}"
            
            elif "SET_FASTIC_CONFIG" in received:
                data = received
                # Okay this shit is actually funny.
                # I have the issue that TCP only allows ~1600 chars, but the FastIC+ config is 305 16bit numbers which are ~1800 when send as ASCII
                # And I cannot use binary because of this dump .encode() and .decode()
                # SO I thought: I know all the data ist just 16bit - so I can use: 255 -> 0xFF -> FF!
                # I always know the legnth of my data blocks and the format and can even save the darm "," between
                # So what I send are just the letters of the integer in hex in one massive autistic block here and reduce the length enough for 1 TCP Comm.
                # And then seperate every pair of letters and convert this back to an integer
                # "Sometimes my genius ... its almost frightening"
                self.configID = data.split(" ")[1]
                raw = data.split(" ")[2]
                config = [int(raw[i:i+2],16) for i in range(0, len(raw), 2)]
                
                log("Config rcv.! :",config[:5],"...",len(config))
                self.FastIC.write_calib(config)
                self.FastIC.write_config(config)
                
                self.FastIC_config = self.FastIC.read_config()
                saved_config = self.FastIC.read_calib()
                self.config_status =  int(self.FastIC_config==saved_config)

            self.read_flag = False
            config_writer(self.rtc,[self.max_voltage,self.max_current,self.voltage,self.ramp,self.HVStatus,self.Mode,self.configID,self.device_type])
            
            return "INTERNAL"
        else:
            return "A"
        
    # kill is HUGHLY important
    # This NEEDS to be called when shutting down, because Micropython has some nasty habits of notcorretcly shutting down multi core processes
    def kill(self):
        self.runFlag = False
        gc.collect()
        _thread.exit()