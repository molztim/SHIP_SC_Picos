import time

def laserserver(request,laser,calib,lastdata,laserstatus,modecontrol,fast):
    #data = laser.read() + calib
    if "GET_" in request:
        if "DIST" in request:
            if laserstatus and modecontrol:
                dist = []
                for _ in range(6):
                    #time.sleep_ms(180)
                    dist += [laser.read()*1000]                 
                mw = sum(dist)/len(dist)  
                data = mw+ calib
                response = "{:.0f}".format(data)
            else:
                response = "{:.0f}".format(lastdata)
                #response = "{:.0f}".format(42)
        elif "STATUS" in request:
            response = "{}".format(int(laserstatus))
        elif "FAST" in request:
            response = "{}".format(int(fast))
            
            
    elif "SET_" in request:
        if "DIST" in request:
            data = laser.read() + calib
            newDistance = int(request.split(" ")[1])
            response = "INTERNAL:{}:{}".format(newDistance,data)
        elif "STAT" in request:
            newstatus = int(request.split(" ")[1])
            if newstatus:
                confirmed_status = laser.laserON()
            else:
                confirmed_status = laser.laserOFF()
            response = "INTERNAL:{}".format(confirmed_status)
        elif "MODE" in request:
            newmode = int(request.split(" ")[1])
            response = "INTERNAL:{}".format(newmode)
            
            
        
    else:
        response = "8000"
        time.sleep_ms(250)
    return response