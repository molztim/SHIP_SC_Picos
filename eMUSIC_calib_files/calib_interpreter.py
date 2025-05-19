path = "/home/sbt/Documents/eMUSIC_calib_files/deviceG2_LG.calib"
file = open(path,"r")
data = [int(x) for x in file.read().split(", ")]
file.close()

CONFIG_KEY_LIST = ['LOWATLAD_PZ', 'VDCHG', 'VDCLG', 'VCM', 'VDCCH', 'IBCOMP', 'VBG_ADJ', 'IBOP_SE', 'IBAB_SE', 'FASTOR', 'HLSUMHG', 'ENDIFFDRVHG', 'ENBYPASSHG', 'ENPZHG', 'HLSUMLG', 'ENDIFFDRVLG', 'ENBYPASSLG', 'ENPZLG','ENCHSUM', 'VLIM', 'CAPPZ', 'RLAD', 'IBAB_DIFF', 'IBOP_DIFF', 'IBPAIR', 'IBAB_PZ', 'IBIN', 'IBPZ_BUF', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP', 'ENCH', 'DISIN', 'DVOFFSET', 'HLANA', 'ENCHSW', 'ENPZ', 'ENDRVSE', 'DVTH', 'PHLCOMP', 'PENCOMPSW', 'PENZPZCOMP']
EMUSIC_CONFIG_HGLG = [1, 144, 144, 111, 120, 3, 6, 3, 15, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 38, 31, 3, 15, 3, 4, 4, 25, 3, 1, 0, 244, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 236, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 240, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 228, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 224, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 232, 1, 1, 1, 1, 120, 1, 0, 1, 1, 0, 229, 1, 1, 1, 1, 120, 1, 0, 1] 

a = 0
for k,v,nv in zip(CONFIG_KEY_LIST,EMUSIC_CONFIG_HGLG,data):
    #print(f"{k}: {v} / {nv}",end="")
    if v != nv:
        print(f"{k}: {v} / {nv}",end="")
        print(" [x]")

        if k == "HLANA": 
            a+=1
            print(a)
    #else:
        #print()
