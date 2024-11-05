import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Parse command-line arguments.")
parser.add_argument("-e", type=int, help="Which eMUSIC are we going to configure?",required=True)
parser.add_argument("-p", type=int, help="What is the SIPM Power & Control board ID",required=True)
parser.add_argument("-d", type=int, help="Shall we use digital? (Yes/No)?", default=0)
parser.add_argument("-th", type=int, help="Threshold in mV",default=25)

# Parse arguments
args = parser.parse_args()

# Print the values of e, d, and th
print(f"Generate Configuration for EMUSIC {args.e}. Run Digital? {args.d} Threshold? {args.th} mV")

# This is the main, new Configuration
EMUSIC_CONFIG_HGLG = [1, 144, 144, 111, 120, 3, 6, 3, 15, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 38, 31, 3, 15, 3, 4, 4, 25, 3, 1, 0, 244, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 236, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 228, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 224, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 232, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 229, 1, 1, 1, 1, 120, 1, 0, 1] 
CONFIG_KEY_LIST = ['LOWATLAD_PZ', 'VDCHG', 'VDCLG', 'VCM', 'VDCCH', 'IBCOMP', 'VBG_ADJ', 'IBOP_SE', 'IBAB_SE', 'FASTOR', 'HLSUMHG', 'ENDIFFDRVHG', 'ENBYPASSHG', 'ENPZHG', 'HLSUMLG', 'ENDIFFDRVLG', 'ENBYPASSLG', 'ENPZLG','ENCHSUM', 'VLIM', 'CAPPZ', 'RLAD', 'IBAB_DIFF', 'IBOP_DIFF', 'IBPAIR', 'IBAB_PZ', 'IBIN', 'IBPZ_BUF', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP']

new_config = [e for e in EMUSIC_CONFIG_HGLG]

def change(k,v):
    print(f"Set '{k}' [{CONFIG_KEY_LIST.index(k)}] to  {v} / {bin(v)}")
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


threshold_fit_values = {
    "2" : [[-0.283, 76.438],[-0.273, 79.138],[-0.267, 79.362],[-0.266, 72.112],[-0.223, 55.613],[-0.271, 71.312],[-0.266, 75.987],[-0.283, 77.288]],
    "11": [[-0.275, 84.663],[-0.292, 89.288],[-0.291, 90.413],[-0.300, 91.938],[-0.304, 94.237],[-0.314, 97.713],[-0.311, 96.463],[-0.282, 86.062]],
    "14": [[-0.251, 58.038],[-0.246, 57.238],[-0.280, 65.013],[-0.260, 62.688],[-0.260, 65.237],[-0.264, 64.338],[-0.253, 62.787],[-0.257, 61.288]],
    "1" : [[-0.279, 76.913],[-0.284, 79.038],[-0.299, 83.838],[-0.295, 84.588],[-0.296, 83.588],[-0.302, 86.388],[-0.296, 84.962],[-0.296, 83.688]],
    "6" : [[-0.249, 81.388],[-0.272, 87.538],[-0.274, 87.663],[-0.247, 81.363],[-0.241, 79.888],[-0.246, 81.438],[-0.242, 80.188],[-0.260, 83.838]],
    "7" : [[-0.263, 79.162],[-0.261, 78.963],[-0.254, 77.438],[-0.259, 80.763],[-0.262, 82.213],[-0.263, 82.063],[-0.265, 82.688],[-0.274, 84.263]],
    "20" : [[-0.247, 70.713],[-0.259, 73.612],[-0.270, 77.812],[-0.254, 73.738],[-0.260, 76.388],[-0.262, 77.188],[-0.261, 77.038],[-0.255, 74.188]],

}

def threshold_calc(Vth,eMUSIC):
    #Vth = a*DVTH + b
    #DVTH = (Vth - b) / a
    DVTH = [0]*8
    try:
        values = threshold_fit_values[eMUSIC]
    except:
        print(f"WARNING! No Threshold Measurement found for eMUSIC #{select_eMUSIC}. Check input or database")
        return DVTH
    DVTH = [round((Vth - parameter[1]) / parameter[0]) for parameter in values]
    for i,v in enumerate(DVTH):
        if v < 0:
            print(f"WARNING! You use a threshold the eMUSIC cannot set on CH {i}! Max Threhsold {min([e[1] for e in threshold_fit_values[eMUSIC]])}")    
        return DVTH

offset_list = {
    "3" : [213, 204, 203, 200, 202, 217, 209, 206],
    "12": [200, 202, 212, 201, 209, 196, 183, 183],
    "2" : [186, 193, 208, 211, 180, 193, 176, 167],
    "11" : [195, 193, 188, 202, 204, 219, 216, 208],
    "14" : [205, 197, 212, 206, 203, 223, 222, 211],
    "1" : [177, 191, 204, 204, 204, 209, 184, 187],
    "4" : [183, 196, 198, 199, 197, 202, 214, 197],
    "6" : [173, 173, 187, 193, 194, 221, 206, 194],
    "7" : [173, 184, 199, 190, 163, 165, 163, 152],
    "20" : [181, 199, 178, 190, 183, 193, 195, 180],
    "4" : [177, 186, 182, 185, 184, 188, 215, 193]
    }

select_eMUSIC = str(args.e)
digi = args.d
threshold = args.th #mV

dvth_list = threshold_calc(threshold,select_eMUSIC)

print("\n ----- Changes made to the original ---- \n")

change("RLAD",3) #3 in analog, 5 in digi
change("CAPPZ",31) #31 in analog, 12 / 31 in digi
change("VBG_ADJ",0) # [0,7]

if select_eMUSIC not in offset_list.keys():
    raise RuntimeError(f"No offset found for this EMUSIC {select_eMUSIC}!\n-----------------\nTERMINATING GENERATION\n------------------")

for i,offset in enumerate(offset_list[select_eMUSIC]):
    changeCH("DVOFFSET",offset,ch=i+1)

for i,DVTH in enumerate(dvth_list):
    changeCH("DVTH",DVTH,ch=i+1)

if digi:
    changeAllCH("ENDRVSE",0)
    changeAllCH("PENCOMPSW",1)
    changeAllCH("PENZPZCOMP",0)
else:
    changeAllCH("ENDRVSE",1)
    changeAllCH("PENCOMPSW",0)
    changeAllCH("PENZPZCOMP",1)

print("\n ----- The new configuration file ---- \n")


for k,v,nv in zip(CONFIG_KEY_LIST,EMUSIC_CONFIG_HGLG,new_config):
    if k == "ENCH":
        break
    print(f"{k}: {nv}",end="")
    if v != nv:
        print(" [x]")
    else:
        print()

print("\n ----- The 8 channels in the new file ---- \n")


for i,k in enumerate(CONFIG_KEY_LIST[105:]):
    print(k,end=": ")
    for pos in list(range(24+4+i,24+i+4+11*8,11)):
        print(new_config[pos], end=" ")
    print()

#new_file = open(f"EMUSIC{select_eMUSIC}_calib.calib","w")
new_file = open(f"device{args.p}.calib","w")
new_file.write(", ".join(str(v) for v in new_config))
new_file.close()
print("Generated File")