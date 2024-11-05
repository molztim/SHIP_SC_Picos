from pico_utils import *
import gc
import _thread
import utime
import random as r
from machine import Pin,I2C,ADC
from eMUSIC_register_mod import *
from I2C_CAEN import A7585
from eMUSIC_mod import eMUSIC 

print("--- eMUSIC New Calib Maker ---")
def change(k,v):
    print(f"Set '{k}' {CONFIG_KEY_LIST.index(k)} => {v} / {bin(v)}")
    new_config[CONFIG_KEY_LIST.index(k)] = v
    
def change8(k,v):
    print(f"Set '{k} Ch 8' {CONFIG_KEY_LIST.index(k)} => {v} / {bin(v)}")
    new_config[105+CONFIG_KEY_LIST[-11:].index(k)] = v
    
def changeAllCH(k,v):
    print(f"Set '{k} All Ch' {CONFIG_KEY_LIST.index(k)} => {v} / {bin(v)}")
    pos = CONFIG_KEY_LIST[28:].index(k)
    for i in range(8):
        new_config[28+i*11+pos] = v
        
def changeCH(k,v,ch=8):
    print(f"Set '{k} Ch {ch}' {CONFIG_KEY_LIST.index(k)} => {v} / {bin(v)}")
    pos = CONFIG_KEY_LIST[28:].index(k)
    new_config[28+(ch-1)*11+pos] = v
    
def loader(path):
    loaded_config = []
    with open(path, 'r') as file:
        for line in file:
            if line[0] in ["#","\n"]:
                continue
            elif "HL_SUM" in line or "EN_DIFF_DRV_HL" in line or "EN_BYPASS_HL" in line or "EN_PZ_HL" in line:
                data = int(line.split("= ")[1].replace("\n",""))
                loaded_config.append((data & 0b10) >> 1)
                loaded_config.append(data & 0b01)
            else:
                loaded_config.append(int(line.split("= ")[1].replace("\n","")))
                
    file.close()
    #print(loaded_config)
    return loaded_config

def findthreshold(target):
    best_guess = [0,0,100]
    for VBG_ADJ in range(8):
        for DVTH in range(2**9):
            Vth = 1.5 * (VBG_ADJ * 0.3) - 1.64/2 + (0.00316 / 2 * DVTH)
            if abs(Vth - target) < abs(best_guess[-1] - target):
                best_guess = [VBG_ADJ,DVTH,Vth]
    print(f"Finished Guessing! VBG_ADJ {best_guess[0]}, DVTH: {best_guess[1]}, Target: {target}/{best_guess[2]} V")
    return  best_guess
    


    

original = EMUSIC_CONFIG_HGLG
#[1, 144, 144, 111, 120, 3, 6, 3, 15, 0, 3, 0, 0, 3, 0, 38, 31, 3, 15, 3, 4, 4, 25, 3, 1, 0, 244, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 236, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 228, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 224, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 232, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 229, 1, 1, 1, 1, 120, 1, 0, 1]
#CONFIG_KEY_LIST = ['LOWATLAD_PZ', 'VDCHG', 'VDCLG', 'VCM', 'VDCCH', 'IBCOMP', 'VBG_ADJ', 'IBOP_SE', 'IBAB_SE', 'FASTOR', 'HLSUMHG', 'ENDIFFDRVHG', 'ENBYPASSHG', 'ENPZHG', 'HLSUMLG', 'ENDIFFDRVLG', 'ENBYPASSLG', 'ENPZLG','ENCHSUM', 'VLIM', 'CAPPZ', 'RLAD', 'IBAB_DIFF', 'IBOP_DIFF', 'IBPAIR', 'IBAB_PZ', 'IBIN', 'IBPZ_BUF', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP']

#VBG_ADJ, DVTH, bestVth = findthreshold(0.) #V
VBG_ADJ = 0 # Lower Bound: 4
DVTH = 200 #Lower Bound: 65
digi = 1

# Third measurement
# 0 / 0 - 23 mV
# 0 / 50 - ?

# 1 / 500 - 


# Set Registers, adjust laser intensity and find threshol
# VBG_ADJ / DVTH ~ Laser Intensity ~ Peak
# 2 / 0 ~ 49.2% ~ 30mV
# 2 / 100 ~ 42.6% ~ 50mV
# 2 / 250 ~ 30.2% ~ 10 mV
# 1 / 0 ~ 69.8% ~ 150mV
# 1 / 100 ~ 62.2% ~ 130 mV
# 1 / 200 ~ 52% ~ 100 mV
# 1 / 300 ~ 45.8% ~ 80mV
# 1 / 400 ~ 34% ~ 40 mV
# 0 / 0 ~ 70.6% ~ 140 mV
# 0 / 100 ~ 61.2% ~ 120 mV
# 0 / 200 ~ 52% ~ 100 mV
# 0 / 300 ~ 46% ~ 80 mV
# 0 / 400 ~ 35% ~ 42 mV
# 0 / 500 ~ 30% ~ 20mV

# 1 / 0 ~ 150 mV
# 2 / 0 ~ 80 mV
# 3 / 0 ~ 80 mV
# 4 / 0 ~ 31 % ~ 20mV
# 5 / 0 ~ 31% ~ 20 mV
# 6 / 0 ~ 49% ~  UKN mV
# 7 / 0 ~ 49% ~  UKN mV

# 1 / 100 ~ 61.42% ~ 140 mV
# 2 / 100 ~ 41.63 % ~ 60 mV
# 3 / 100 ~ 40.6% ~ 60 mV
# 4 / 100 No signal found - it triggers on everything. We are beyond the noise threshold here

# Find value for noise threshold. Noise < 10mV
# 4 / 60 until 65

# Set Threshold to wrong value, then adjust Laser Intensity to find threshold
# 90mV Peak ~ 0V TH ~ 53% Laser ~ 1 / 234
# 70mV-75mV ~ 100mV TH ~ 49% ~ 2 / 13
# 60mV Peak ~ 200mV "Threshold" ~ 45.4% Laser ~ 2 / 76
# 25-30mV Peak ~ 300mV "Threshold" ~ 33.4% Laser ~ 1 / 424
# 15mV Peak ~ 400mV TH ~ 31% ~ 1 /
# 15mV Peak ~ 500mV TH ~ 


# For 60% Laser at 100mV (+15%)
# 0.1V = 60ns
# 0.2V = 90ns
# 0.3V = 200 / XXX ns
# 0.4V = 600ns
# 0.5V = Verrückt
# 0.6V = Rauschen

# For 100% Laser 200mV (+15%)
# 0.01V = 140ns
# 0.02V = 140ns
# 0.03V = 140ns
# 0.05V = 140ns
# 0.075V = 140ns
# 0.09V = 140ns
# 0.1V = 160ns
# 0.2V = 200ns
# 0.3V = 300ns
# 0.4V = 400ns
# 0.5V = 420ns
# 0.6V = Crazy

EMUSIC = eMUSIC(17,18,16,19)

new_config = [e for e in original]

#new_config = loader("digi1.txt")

#Digital Analyse

change("RLAD",3) #3 in analog, 5 in digi
change("CAPPZ",31) #31 in analog, 12 / 31 in digi

# From main body
#change("VCM",150)
#change("VDCCH",100)
#change("ENDIFFDRVHG",0)
#change("ENBYPASSHG",0)
#change("HLSUMLG",0)
#change("ENCHSUM",255)


#change("IBAB_SE",15)
#change("IBOP_SE",3)
change("VBG_ADJ",VBG_ADJ) # [0,7]
#change("IBCOMP",0) # [0,7]

# Vth = 1.5 * [VBG_ADJ * 0.3V] - 1.64/2 V + [0.00316/2 V * DVTH]

# From Channel 8 settings
#changeCH("ENCH",1)
#changeCH("DISIN",0)
#changeCH("DVOFFSET",200)
#changeCH("HLANA",1)
#changeCH("ENCHSW",1)
#changeCH("ENPZ",1)

changeAllCH("ENDRVSE",1)
changeAllCH("PENCOMPSW",0)
changeAllCH("PENZPZCOMP",1)


if digi:
    change8("ENDRVSE",0)
    change8("DVTH",DVTH) 
    #change8("PHLCOMP",1)
    change8("PENCOMPSW",1)
    change8("PENZPZCOMP",0)
    
    changeAllCH("ENDRVSE",0)
    changeAllCH("DVTH",DVTH) 
    #changeAllCH("PHLCOMP",1)
    changeAllCH("PENCOMPSW",1)
    changeAllCH("PENZPZCOMP",0)
    
changeCH("DVOFFSET",179,ch=1)
changeCH("DVOFFSET",171,ch=2)
changeCH("DVOFFSET",166,ch=3)
changeCH("DVOFFSET",183,ch=4)
changeCH("DVOFFSET",198,ch=5)
changeCH("DVOFFSET",181,ch=6)
changeCH("DVOFFSET",218,ch=7)
changeCH("DVOFFSET",210,ch=8)


"""
print("\n--- Resulting changes ---\n")
for k,v,nv in zip(CONFIG_KEY_LIST,original,new_config):
    if k == "ENCH":
        break
    print(f"{k}: {v} => {nv}",end="")
    if v != nv:
        print(" [x]")
    else:
        print()
"""  
print("\n--- CH 8 ---\n")

for k,v,nv in zip(CONFIG_KEY_LIST[105:],original[105:],new_config[105:]):
    print(f"{k}: {v} => {nv}",end="")
    if v != nv:
        print(" [x]")
    else:
        print()

for k,v,nv in zip(CONFIG_KEY_LIST,original,new_config):
    if k == "DVOFFSET":
        print(f"{k}: {v} => {nv}",end="")
        if v != nv:
            print(" [x]")
        else:
            print()

print("\n--- eMUSIC writing ---")
print("Writing new Config ...")
EMUSIC.write_config(new_config)
print("Finished!")

print("\n--- eMUSIC reading (sanity check) ---")
local_config = EMUSIC.read_config()
print(f"New Config: {local_config == new_config}")
for k,v,vn in zip(CONFIG_KEY_LIST,local_config,new_config):
    if vn != v:
        print(k,vn,v)
        break
    if k == "DVTH": print(k,v,vn)
