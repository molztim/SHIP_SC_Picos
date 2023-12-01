from time import sleep

def laserserver(request,laser,calib,lastdata,laserstatus):
    #data = laser.read() + calib
    if "GET_" in request:
        if "DIST" in request:
            if laserstatus:
                data = laser.read() + calib
                response = "{}".format(data)
            else:
                response = "{}".format(lastdata)
        elif "STATUS" in request:
            response = "{}".format(int(laserstatus))
            
            
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
            
        
    else:
        response = "8000"
    return response