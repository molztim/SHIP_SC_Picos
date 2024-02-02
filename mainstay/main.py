import socket
import time
from pico_ultis import *
from machine import Pin, I2C, soft_reset, reset
#from laser_device import device
from machine import RTC
import _thread
import gc

rtc = RTC()

led = Pin("LED", Pin.OUT,value=1)

SSID = 'SHIP_PicoNet'
PASS = 'ThereIsAlwaysABiggerFish'

sensor_file = None
second_thread = None
sensor = None

ID = "EMERGENCY - 10.42.0.199"
IP = ('10.42.0.199' ,'255.255.255.0','10.42.0.1','10.42.0.1')
wlan_ips = '0.0.0.0'

memory = os.listdir()
sensor_list = [file_name for file_name in memory if "_device" in file_name and file_name != "test_device"]
log("Sensor software onboard: sensor_list")
if len(sensor_list) == 0:
    log("No device file found!")
    error_log("No device file found!")
elif len(sensor_list) > 1:
    log("Device ambigouse!")
    error_log("Device ambigouse!")
else:
    log("Found device!")
    sensor_file = sensor_list[0].replace(".py","")

if sensor_file:
    try:
        sensor_module = __import__(sensor_file)
        device = getattr(sensor_module, "device")
        #Activate device
        sensor = device(rtc)
        log(f"Sensor with object {sensor} active and thread running!")
        ID = sensor.getID() 
        IP = (sensor.getIP() ,'255.255.255.0','10.42.0.1','10.42.0.1')
    except Exception as e: 
        log(f"Device not found/init! {e}")
        error_log(f"Device not found/init! {e}")

for i in range(5):
    try:
        wlan_ips = t_wlan(SSID,PASS,IP)
        log("Device IP:",wlan_ips[0])
        time.sleep_ms(5)
        break
    except Exception as e:
        blink(led)
        log("No network conenction found!")
        error_log(f"No network conenction found! {e}")

if wlan_ips == '0.0.0.0':
    time.sleep(60)
    soft_reset()

    
led.off()

try:
    #Start Server socket
    addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
    s = socket.socket()
    s.bind(('',80))
    #I hope this socket command solves the EADDRINUSE errors
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(5)
    log('Socket listening on', addr)
except Exception as e:
    log(f"Socket Starting Error: {e}")
    error_log(f"Socket Starting Error: {e}")
    soft_reset() 

#Lets get the sensor running

if sensor:
    try:
        second_thread = _thread.start_new_thread(sensor.measurement, ())
    except Exception as e:
        log(f"Second Core did not start working! {e}")
        error_log(f"Second Core did not start working! {e}")

#Enter main loop
log("Ready for operation!")
try:    
    while True:
        cl, addr = s.accept()
        while True:
            try:
                package = cl.recv(1024)
                rcv = package.decode('utf-8')
                if rcv == "":
                    break
                log("Received bytes:",rcv)

                #This code allows to reporgram the system via WiFi by pushing code
                response = "DUMMY"
                if "NEW_DATA" in rcv:
                    rcv_new_file(rcv)
                    response = "INTERNAL"
                elif "RESTART" in rcv:
                    response = reprogramm(rcv)
                elif "NEW_SOFTWARE" in rcv:
                    response = blank()
                elif "ERROR_LOG" in rcv:
                    response = fetch_errorlog()
                elif "BLINK" in rcv:
                    blink(led)
                    response = "INTERNAL"
                elif "IDENTIFY" in rcv:
                    response = ID
                else:
                    if sensor:
                        try:
                            response = sensor.server(rcv)
                        except Exception as e:
                            log(f"Sensor server failed! {e}")
                            error_log(f"Sensor server failed! {e}")
                cl.send(response+'\r')
                if "TEST" not in rcv and response == "REPROGRAM":
                    log("Restart!")
                    reset()
            except Exception as e:
                #Close socket (must have!)
                log("Close interaction with: {}\n".format(e))
                #if sensor and second_thread:
                #    log("Kill Cores #0 and #1")
                #    sensor.kill()
                cl.close()
                #s.close()
                time.sleep(1)
                break
except Exception as e:
    log(f"Exit mainloop with error {e}.")
finally:
    log(f"Exit mainloop.")
    if sensor and second_thread:
        log("Kill Cores #0 and #1")
        sensor.kill()
    time.sleep(0.2)
    s.close()
    soft_reset()
