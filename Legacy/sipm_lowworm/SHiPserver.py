from eMUSIC_registers import *
import utime as time

def timetest(request,DEV,enable_Pin):
    if request == "GET_HVON":           
        statusHV = DEV.GetHVOn()            
        return "{}".format(int(statusHV==True))
    elif "SET_ENA" in request:
        ENA = int(request.split(" ")[1])
        enable_Pin.value(ENA)
        statusHV = DEV.GetHVOn()
        response = "{}".format(statusHV)
    else:
        return "{}".format(0)

def webserver(request,DEV,EMUSIC,enable_Pin):
    #start = time.ticks_us()
    data_string="WARNING"
    response = ""
    if "GET_" in request:
        if request == "GET_VOUT":
            Vout = DEV.GetVout()
            response = "{:.2f}".format(Vout)
        elif request == "GET_HVON":
            statusHV = DEV.GetHVOn()            
            response = "{}".format(int(statusHV==True))
        elif request == "GET_CON":
            connectionHV = DEV.GetConnectionStatus()
            response = "{}".format(int(connectionHV==True))
        elif request == "GET_IOUT":
            Iout = DEV.GetIout()
            response = "{:.2f}".format(Iout)
        elif request == "GET_VIN":
            Vin = DEV.GetVin()
            response = "{:.2f}".format(Vin)
        elif request == "GET_RAMP":
            Vrmp = DEV.GetRampVs()
            response = "{:.2f}".format(Vrmp)
        elif request == "GET_MAXV":
            maxV = DEV.GetMaxV()
            response = "{:.2f}".format(maxV)
            
        elif request == "GET_HV_M":
            Vout = DEV.GetVout()
            Iout = DEV.GetIout()
            Vin = DEV.GetVin()
            statusHV = DEV.GetHVOn()
            connectionHV = DEV.GetConnectionStatus()
            #response = bytearray([int(Vout), int(Iout), int(Vin), int(statusHV), int(connectionHV)])
            response = "{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(Vout,Iout,Vin,statusHV,connectionHV).encode('utf-8')
            
##############################            
#Begin of GET eMUSIC commands#
##############################
            
        elif request == "GET_EMUSIC":
            current_config = EMUSIC.read_config()
            saved_config = EMUSIC.read_calib()
            if current_config == saved_config:
                response = "{}".format(int(True))
            else:
                response = "{}".format(int(False))
                
        elif request[:-1] == "GET_ENCH":
            ch = int(request[-1])-1 #Why is this? Because the channel go on doberview 1-8, but in code 0-7
            status = EMUSIC.read_eMUSIC("ENCH",channel = ch)
            if status == 1:
                response = "{}".format(int(True))
            else:
                response = "{}".format(int(False))
                
        elif request[:-1] == "GET_PZCH":
            ch = int(request[-1])-1
            status = EMUSIC.read_eMUSIC("ENPZ",channel = ch)
            if status == 1:
                response = "{}".format(int(True))
            else:
                response = "{}".format(int(False))
                
        elif request == "GET_LOWAT":
            status = EMUSIC.read_eMUSIC("LOWATLAD_PZ")
            if EMUSIC_CONFIG[pos] == 1:
                response = "{}".format(int(True))
            else:
                response = "{}".format(int(False))
                
        elif request[:-1] == "GET_OFFSETCH":
            ch = int(request[-1])-1
            status = EMUSIC.read_eMUSIC("DVOFFSET",channel = ch)
            response = "{}".format(status)
            
        elif request == "GET_RLADPZ":
            status = EMUSIC.read_eMUSIC("RLAD")
            response = "{}".format(status)
            
        elif request == "GET_CAPPZ":
            status = EMUSIC.read_eMUSIC("CAPPZ")
            response = "{}".format(status)
            
        elif request == "GET_VDCCH":
            status = EMUSIC.read_eMUSIC("VDCCH")
            response = "{}".format(status)
            
        elif request == "GET_ENCH_M":
            current_config = EMUSIC.read_config()
            saved_config = EMUSIC.read_calib()
            
            config_status = [current_config==saved_config]
            
            print(f"\ncurrent_config : {len(current_config)} \nsaved_config {len(saved_config)}\n")
            
            ch_status = current_config[24::11]
            pz_status = current_config[29::11]
            rladpz_status = [current_config[17]]
            capppz_status = [current_config[16]]
            vdcch_status = [current_config[3]]
            lowat_status = [current_config[0]]
            offsset = current_config[26::11]
            print(f"Channels gelesen: {ch_status}")
            response = bytearray(config_status + ch_status + pz_status + rladpz_status + capppz_status + vdcch_status + lowat_status + offsset)

            
        else:
            raise RuntimeError("Couldn't understand doberman's request!")
            
##########################
#All requests to set data#
##########################
            
    elif "SET_" in request:
        if "SET_V" in request:
            Vnew = float(request.split(" ")[1])
            DEV.SetV(Vnew)
            time.sleep(0.1)
            Vout = DEV.GetVout()
            response = "{:.5f}".format(Vout)
            
        elif "SET_MAXV" in request:
            Vnew = float(request.split(" ")[1])
            DEV.SetMaxV(Vnew)
            time.sleep(0.1)
            response = str(Vnew)
            
        elif "SET_MAXI" in request:
            Inew = float(request.split(" ")[1])
            DEV.SetMaxI(Inew)
            response = str(Inew)
            
        elif "SET_RAMP" in request:
            Rampnew = float(request.split(" ")[1])
            DEV.SetRampVs(Rampnew)
            response = str(Rampnew)
            
        elif "SET_MODE" in request:
            Modenew = int(request.split(" ")[1])
            DEV.SetMode(Modenew)
            response = str(Modenew)
        
        elif "SET_ENA" in request:
            ENA = int(request.split(" ")[1])
            #log("Enable Request {}".format(ENA))
            enable_Pin.value(ENA)
            #log("Immidiate out: {}".format(enable_Pin.value()))
            #DEV.SetEnable(ENA)
            statusHV = DEV.GetHVOn()
            response = "{}".format(statusHV)
            
#########################################
# From here on begin the eMUSIC commands#
#########################################

        elif "SET_CHENABLE" in request:
            ENA = int(request.split(" ")[1])
            CHA = int(request.split(" ")[0][-1])-1
            EMUSIC.write_eMUSIC(ENA,"ENCH",channel = CHA)
            EMUSIC.write_line(ENA,"ENCH",channel = CHA)
            response = "{}".format(ENA)
            
        elif "SET_CHPZ" in request:
            ENA = int(request.split(" ")[1])
            CHA = int(request.split(" ")[0][-1])-1
            EMUSIC.write_eMUSIC(ENA,"ENPZ",channel = CHA)
            response = "{}".format(ENA)
            
        elif "SET_CHOFFSET" in request:
            ENA = int(request.split(" ")[1])
            CHA = int(request.split(" ")[0][-1])-1
            EMUSIC.write_eMUSIC(ENA,"DVOFFSET",channel = CHA)
            response = "{}".format(ENA)
            
        elif "SET_LOWAT" in request:
            ENA = int(request.split(" ")[1])
            EMUSIC.write_eMUSIC(ENA,"LOWATLAD_PZ")
            response = "{}".format(ENA)
            
        elif "SET_VDCCH" in request:
            ENA = int(request.split(" ")[1])
            EMUSIC.write_eMUSIC(ENA,"VDCCH")
            response = "{}".format(ENA)
            
        elif "SET_CAPPPZ" in request:
            ENA = int(request.split(" ")[1])
            EMUSIC.write_eMUSIC(ENA,"CAPPZ")
            response = "{}".format(ENA)
            
        elif "SET_RLADPZ" in request:
            ENA = int(request.split(" ")[1])
            EMUSIC.write_eMUSIC(ENA,"RLAD")
            response = "{}".format(ENA)
        
        elif "SET_eMUSIC" in request:
            data = request.split(" ")[1]
            config = [int(x) for x in data.split(" ",1)[1].replace(" ","")[1:-1].split(",")]
            log("Config rcv.! :",config[:5],"...")
            EMUSIC.write_calib(config)
            EMUSIC.write_config(config)
            response = "1"
            
        else:
            response = data_string
            print("Emtpy")
            
        
    elif "ping" in request:
        response = "Pong! Glowworm 1"
        
    else:
        response = data_string
        print("WARNING WA02: Request not in data base.")
        
    #end = time.ticks_us()
    #diff = time.ticks_diff(end,start)
    #print("Time for operation in webserver:",diff)
    return response