import time

def laserserver(request,laser,calib,lastdata,laserstatus,modecontrol,fast):
    #data = laser.read() + calib
    if "GET_" in request:
        if "DIST" in request:
            print("Sys: ",laserstatus, modecontrol,fast)
            if laserstatus and modecontrol:
                print("do new measurement")
                #dist = []
                #for _ in range(15): #6
                    #time.sleep_ms(180)
                    #mw = laser.read3()*1000
                #print(dist)
                #mw = sum(dist)/len(dist)
                #data = mw+ calib
                data = laser.read3()*1000 + calib 
                response = "{:.0f}".format(data)
            else:
                response = "{:.0f}".format(lastdata)
                print("Use old data...")
                #response = "{:.0f}".format(42)
        elif "STATUS" in request:
            response = "{}".format(int(laserstatus))
        elif "FAST" in request:
            response = "{}".format(int(fast))
            
            
    elif "SET_" in request:
        if "DIST" in request:
            data = laser.read() + calib
            newDistance = -int(request.split(" ")[1])
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