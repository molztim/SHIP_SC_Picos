from machine import UART, Pin
import struct
from utime import sleep

conversion_matrix = {
    'output_voltage' :  ['0000','FFFF',1.812e-3,0,1],
    'output_current' : ['0000','0400',4.980e-3,0,1],
    'mppc_temp' :      ['0000','FFFF', 1.907e-5, 1.035,-5.5e-3],
    '2nd_high_temp' :  ['FC18', '03E8',1.507e-3,0,1],
    '2nd_low_temp' :   ['FC18', '03E8',1.507e-3,0,1],
    '1st_high_temp' :  ['0000','FFFF',5.225e-2,0,1],
    '1st_low_temp' :   ['0000','FFFF',5.225e-2,0,1],
    'ref_voltage' :    ['0000','FFFF',1.812e-3,0,1],
    'ref_temp' :  ['0000','FFFF', 1.907e-5, 1.035,-5.5e-3],
    'status' : ['0000','FFFF',1,0,1],
    'reserve' : ['0000','FFFF',1,0,1],
    'mode' : ['0000', '0001', 1,0,1]
    }

command_matrix = {
    'hst' : [['2nd_high_temp', '2nd_low_temp', '1st_high_temp', '1st_low_temp', 'ref_voltage', 'ref_temp'],[]],
    'hrt' : [[],['2nd_high_temp', '2nd_low_temp', '1st_high_temp', '1st_low_temp', 'ref_voltage', 'ref_temp']],
    'hpo' : [[], ['status','reserve','output_voltage','output_current','mppc_temp']],
    'hgs' : [[],['status']],
    'hgv' : [[],['output_voltage']],
    'hgc' : [[],['output_current']],
    'hgt' : [[],['mppc_temp']],
    'hof' : [[],[]],
    'hon' : [[],[]],
    'hre' : [[],[]],
    'hcm' : [['mode'],[]],
    'hbv' : [['ref_voltage'],[]]
    }

status_matrix = {
    'HV_out': 0,
    'OC-protec' : 1,
    'Out_current' : 2,
    'Temp_conn' : 3,
    'Temp_Lim' : 4,
    'Temp_corr' : 6
    }

class hamamatsu:
    
    def __init__(self, TX, RX,rampup = 5):
        self.STX = 2
        self.ETX = 3
        self.CR  = 13
        self.rampup = rampup #V/s
        
        try:
            self.uart = UART(0, baudrate = 38400, bits = 8, parity = 0, stop = 1, tx=Pin(TX), rx=Pin(RX))
            print('Building UART:', self.uart)
        except Exception as e:
            print("Error:",e, "during __init__")
            
    def statusconverter(self, status):
        status_list = [1 if (int(status) & 2**i) != 0 else 0 for i in range(16)]
        return_list = {}
        for k,v in status_matrix.items():
            return_list[k] = status_list[v]
        return return_list
    
    def rev_data(self,data):        
        def rev(self,s):
            return "" if not(s) else rev(s[1::])+s[0]

        rev_data = []
        for i in data:
            b = bin(i)[2:]
            b ='0'*(8-len(b))+b
            b = int(rev(b),2)
            rev_data += [b]
        return rev_data
    
    def errorinterpreter(self,data):
        if data == b'0001':
            raise RuntimeError('Device returned an error! UART Comm. Error')
        elif data == b'0002':
            raise RuntimeError('Device returned an error! Timeout Error - CR and STX took > 1s')
        elif data == b'0003':
            raise RuntimeError('Device returned an error! Syntax Error - STX issue, or command to long!')
        elif data == b'0004':
            raise RuntimeError('Device returned an error! Checksum do not match')
        elif data == b'0005':
            raise RuntimeError('Device returned an error! Undefined Command')
        elif data == b'0006':
            raise RuntimeError('Device returned an error! Somewhere is not ASCII code used (0-F)')
        elif data == b'0007':
            raise RuntimeError('Device returned an error! Parameter Size is wrong')
        else:
            raise RuntimeError('Device returned an error! No F*cking Idea!')
        return None
    
    def write_ham(self,asciicommand,data = None):
        
        command = [ord(c.upper()) for c in asciicommand]
        
        value_list = []
        if command_matrix[asciicommand.lower()][0] == []:
            None
        else:
            for regi, datablock in zip(command_matrix[asciicommand][0],data):
                conversion = conversion_matrix[regi]
                value = hex(round((datablock *  conversion[4] + conversion[3]) / conversion[2] + int(conversion[0],16)))[2:].upper()
                value = [ord(i) for i in value]
                value_list += value
        command_checksum = sum(command)
        value_checksum = sum(value_list)

        int_checksum = self.STX + command_checksum + value_checksum + self.ETX
        list_checksum = [ord(ch.upper()) for ch in hex(int_checksum)[-2:]]
        data = bytearray([self.STX] + command + value_list +[self.ETX] + list_checksum + [self.CR])
        self.uart.write(data)
        print("\nData send:",data)
        return None
    
    def read_ham(self):
        rxData = self.uart.readline()
        if rxData == None:
             raise RuntimeError("There is only None on the line!")
        print("Rcv. Data: ",rxData)
        decode_list = rxData[:-3]
        command = str(decode_list[1:4], 'ascii')
        data = decode_list[4:-1]
        print("Liste ohne Checksumme: ",decode_list," Kommando: ",command,"Data: ",data)
        
        if command == 'hxx':
            self.errorinterpreter(data)
        #Check Checksums
        checksum =  rxData[-3:-1]
        #print(checksum)
        #rcv_checksum = hex(sum([ord(element) for element in data]))[-2:]
        rcv_checksum = bytes(hex(sum([int(str(i)) for i in decode_list])).upper()[-2:], 'ascii')
        #print(rcv_checksum,checksum)
        if not rcv_checksum == checksum:
            raise RuntimeError

        #Check for lenght in transmission
        if len(data) == 0.0:
            return [0]
        elif not len(data)/4 == int(len(data)/4):
            raise RuntimeError

        #Data Processing
        data = [data[i:i+4] for i in range(0, len(data), 4)]
        data_conv = command_matrix[command][1]
        #print(data_conv)

        return_list = []
        for value, command in zip(data,data_conv):
            conversion = conversion_matrix[command]
            value = ((int(value, 16) - int(conversion[0], 16)) * conversion[2] - conversion[3]) / conversion[4]
            return_list += [value]
        return dict(zip(data_conv,return_list))
    
    def command(self,command):
        self.write_ham(command)
        sleep(0.01)
        data = self.read_ham()
        return data
    
    def readuart(self,l=0):
        if l == 0:
            return self.uart.readline()
        else:
            return self.uart.read(l)
    
    def writeuart(self,data):
        return self.uart.write(bytearray(data))
    
    def change_voltage(self,new_voltage):
        sleep(1)
        now = self.GetVout()
        print(now, new_voltage, self.rampup, abs(now - new_voltage) > self.rampup)
        if abs(now - new_voltage) > self.rampup:
            print("Going down the ladder")
            if now > new_voltage:
                self.V(now - self.rampup)
                self.change_voltage(new_voltage)
            elif now < new_voltage:
                self.V(now + self.rampup)
                self.change_voltage(new_voltage)
            else:
                print("F*CK!")
        else:
            print("Final step")
            self.V(new_voltage)
        return None
    
##### Setters #####################################################
    
    def SetHVOn(self):
        cmd = 'hon' 
        self.write_ham(cmd)
        sleep(0.1)
        na = self.read_ham()
        return None
    
    def SetHVOff(self):
        cmd = 'hof' 
        self.write_ham(cmd)
        sleep(0.1)
        na = self.read_ham()
        return None
    
    def V(self, v):
        cmd = 'hbv'
        self.write_ham(cmd, [v])
        sleep(0.1)
        na = self.read_ham()
        return None
    
    def SetV(self,v):
        self.change_voltage(v)
        return None
    
    def SetMaxV(self, v):
        return None
    
    def SetMaxI(self, i):
        return None
    
    def SetEnable(self, on):
        #Solved in SHIPServer
        return None
    
    def SetRampVs(self, vs):
        self.rampup = vs
        return None
    
    def SetMode(self, m):
        return None
        
    def SetTemperatureSensor(self,H2,L2,H1,L1,V,T):
        cmd = 'hst'
        self.write_ham(cmd,[H2,L2,H1,L1,V,T])
        sleep(0.1)
        v = self.read_ham()
        return None
            
    def SetSIPMtcoef(self,tcomp):
        self.SetNIPMRegFloat(NIPMREG_TCOEF, tcomp)
    
####### Getters ####################################################
    
    def GetVin(self):
        v = 8000
        return v
    
    def GetVout(self):
        cmd = 'HGV'
        self.write_ham(cmd)
        sleep(0.1)
        v = self.read_ham()['output_voltage']
        return v
    
    def GetIout(self):
        cmd = 'HGC'
        self.write_ham(cmd)
        sleep(0.1)
        i = self.read_ham()['output_current']
        return i
    
    def GetHVOn(self):
        cmd = 'hpo'
        self.write_ham(cmd)
        sleep(0.1)
        status = self.read_ham()['status']
        b = self.statusconverter(status)['HV_out'] # 'HV_out','Out_current','Temp_corr','Temp_Lim','Temp_conn','OC-protec'
        return b
    
    def GetConnectionStatus(self):
        try:
            x = self.GetHVOn
            return 1
        except:
            return 0
        
    def GetT(self):
        cmd = 'HGT'
        self.write_ham(cmd)
        sleep(0.1)
        status = self.read_ham()['mppc_temp']
        t = self.statusconverter(status) # 'HV_out','Out_current','Temp_corr','Temp_Lim','Temp_conn','OC-protec'
        return t
    
    def GetTref(self):
        cmd = 'HRT'
        self.write_ham(cmd)
        sleep(0.1)
        temprefs = self.read_ham()
        return temprefs
    
    def GetVcorrection(self):
        return None
    
    def GetRampVs(self):
        return self.rampup
    
    def GetMaxV(self):
        return 95

    def startup(self,V,rampuptime):
        self.SetV(V,rampup = rampuptime)
        return True
        
    
