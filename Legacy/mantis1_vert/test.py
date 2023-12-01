from laserreangefinder import laserrangefinder
import time
laser = laserrangefinder()
laser.laserON()

interval = 1



for i in range(30):
    try:
        start = time.ticks_ms()
        dist = []
        for _ in range(6):
            time.sleep_ms(180)
            
            dist += [laser.read()*1000]         

        
        mw = sum(dist)/len(dist)               
        stop = time.ticks_ms()
        print(f"{mw} mm")
        print("Time Diff.",time.ticks_diff(stop,start),"ms")
        
        
        #f = open("test.txt","a")
        #f.write(f"{mw}, ")
        #f.close()
        print(f"Measurement {i}")
        time.sleep(interval)
    except KeyboardInterrupt:
        laser.laserOFF()
        sys.exit()
print("Fin!")
laser.laserOFF()     

    
