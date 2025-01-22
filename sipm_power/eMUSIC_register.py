###################
# V2 EMUSIC REGISTER MAPS
####################

R1 = [0,1,2,3,4,5,6,7]
R2 = [8,9,10,11,12,13,14,15]

EMUSIC_CONFIG_HGLG = [1, 144, 144, 111, 120, 3, 6, 3, 15, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 38, 31, 3, 15, 3, 4, 4, 25, 3, 1, 0, 244, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 236, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 228, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 224, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 232, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 229, 1, 1, 1, 1, 120, 1, 0, 1] 
CONFIG_KEY_LIST = ['LOWATLAD_PZ', 'VDCHG', 'VDCLG', 'VCM', 'VDCCH', 'IBCOMP', 'VBG_ADJ', 'IBOP_SE', 'IBAB_SE', 'FASTOR', 'HLSUMHG', 'ENDIFFDRVHG', 'ENBYPASSHG', 'ENPZHG', 'HLSUMLG', 'ENDIFFDRVLG', 'ENBYPASSLG', 'ENPZLG','ENCHSUM', 'VLIM', 'CAPPZ', 'RLAD', 'IBAB_DIFF', 'IBOP_DIFF', 'IBPAIR', 'IBAB_PZ', 'IBIN', 'IBPZ_BUF', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP']

eMUSIC_configfile = {
    #For the individual channel
    "ENCH" : list(range(24+4,24+4+11*8,11)), #Enables or disables channel output [0/1]
    "DISIN" : list(range(25+4,25+4+11*8,11)), #Switch to DISABLE SIPMs. So DISIN=0 => ACTIVE SIPM, DISN=1 => OFF SIPM
    "DVOFFSET" : list(range(26+4,26+4+11*8,11)), #Offset voltage in 9bits [0,511]
    "HLANA" : list(range(27+4,27+4+11*8,11)),#SE Analog Gain selection
    "ENCHSW" : list(range(28+4,28+4+11*8,11)), #Channel enable #2, do not use!
    "ENPZ" : list(range(29+4,29+4+11*8,11)), #Enable PZ Shaper [0,1]
    "ENDRVSE" : list(range(30+4,30+4+11*8,11)), #Enables SE Driver
    "DVTH" : list(range(31+4,31+4+11*8,11)), #Threshold voltage for comparator
    "PHLCOMP" : list(range(32+4,32+4+11*8,11)), #Comparator gain selection
    "PENCOMPSW" : list(range(33+4,33+4+11*8,11)), # Comperator On/Off
    "PENZPZCOMP" : list(range(34+4,34+4+11*8,11)), #Comperator on PZ signal Enable
    
    #The overall registers
    "LOWATLAD_PZ" : [0],
    "VDCHG" : [1],
    "VDCLG" : [2],
    "VCM" : [3],
    "VDCCH" : [4],
    "IBCOMP" : [5],
    "VBG_ADJ" : [6],
    "IBOP_SE" : [7],
    "IBAB_SE" : [8],
    "FASTOR" : [9],
    "HLSUMHG" : [10],
    "ENDIFFDRVHG" : [11],
    "ENBYPASSHG" : [12],
    "ENPZHG" : [13],
    
    "HLSUMLG" : [14],
    "ENDIFFDRVLG" : [15],
    "ENBYPASSLG" : [16],
    "ENPZLG" : [17],
    
    #Missing in reg: ENPZ LG, ENBY LG, ENDIFFDRV LG,  HLSUM LG
    #My guess: ENPZHG, ENBYHG, ENDIFFDRVHG and HLSUM are actually 2 bits - one from HG, the other one is LG, expressed in one int
    #However, for the purpose of testing them,  will activate them here
    
    "ENCHSUM" : [14+4],
    "VLIM" : [15+4],
    "CAPPZ" : [16+4],
    "RLAD" : [17+4],
    "IBAB_DIFF" : [18+4],
    "IBOP_DIFF" : [19+4],
    "IBPAIR" : [20+4], 
    "IBAB_PZ" : [21+4],
    "IBIN" : [22+4],
    "IBPZ_BUF" : [23+4],   
    }

eMUSIC_register = {
    "DVOFFSET" : (R1,list(range(7,16))),
    "DISIN" : (R1,[6]),
    "ENCH" : (R1,[5]),

    "PENZPZCOMP" : (R2,[15]),
    "PENCOMPSW" : (R2,[14]),
    "PHLCOMP" : (R2,[13]),
    "DVTH" : (R2,list(range(4,13))),
    "ENDRVSE" : (R2,[3]),
    "ENPZ" : (R2,[2]),
    "ENCHSW" : (R2,[1]),
    "HLANA" : (R2,[0]),

    "VDCHG" : ([32],list(range(8,16))),
    "VDCLG" : ([32],list(range(0,8))),

    "VCM" : ([33],list(range(8,16))),
    "VDCCH" : ([33],list(range(0,8))),

    "IBAB_SE" : ([34],list(range(10,16))),
    "IBOP_SE" : ([34],list(range(7,10))),
    "VBG_ADJ" : ([34],list(range(4,7))),
    "IBCOMP" : ([34],list(range(0,4))),

    "ENCHSUM" : ([35],list(range(8,16))),
    "ENPZLG" : ([35],[7]),
    "ENPZHG" : ([35],[6]),
    "ENBYPASSLG" : ([35],[5]),
    "ENBYPASSHG" : ([35],[4]),
    "ENDIFFDRVLG" : ([35],[3]),
    "ENDIFFDRVHG" : ([35],[2]),
    "HLSUMLG" : ([35],[1]),
    "HLSUMHG" : ([35],[0]),
    
    #Note: I suggest that in the config_file, the 2 bits per HG channel are to include the LG  as well. Since we only have 3 or 0 (11 or 00),
    #there order is not important, but the point that all HG are expressed in 2 bits is

    "LOWATLAD_PZ" : ([36],[14]),
    "RLAD" : ([36],list(range(11,14))),
    "CAPPZ" : ([36],list(range(6,11))),
    "VLIM" : ([36],list(range(0,6))),

    "IBPAIR" : ([37],list(range(13,16))),
    "IBOP_DIFF" : ([37],list(range(10,13))),
    "IBAB_DIFF" : ([37],list(range(4,10))),

    "IBPZ_BUF" : ([38],list(range(13,16))),
    "IBIN" : ([38],list(range(7,13))),
    "IBAB_PZ" : ([38],list(range(4,7)))
        
    }

"""
eMUSIC_config_list = [None] * (35+11*7)
for key,value in eMUSIC_configfile.items():
    for number in value:
        eMUSIC_config_list[number] = key
print(eMUSIC_config_list)
"""

