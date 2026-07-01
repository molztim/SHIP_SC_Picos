#Fri 05.06.2026
import socket
import utime
from pico_utils import *
from machine import Pin, I2C, soft_reset, reset
#from laser_device import device
from machine import RTC
import _thread
import gc
import sys

error_log("###New Run Start###")

rtc = RTC()

led = Pin("LED", Pin.OUT,value=1)

SSID = 'SHIP_PicoNet'
PASS = 'ThereIsAlwaysABiggerFish'

sensor_file = None
second_thread = None
sensor = None

ID = "EMERGENCY - 10.42.0.150"
IP = ('10.42.0.150' ,'255.255.255.0','10.42.0.1','10.42.0.1')
wlan_ips = '0.0.0.0'

memory = os.listdir()
sensor_list = [file_name for file_name in memory if "_device" in file_name and file_name != "test_device"]
log(f"Sensor software onboard: {sensor_list}")
if len(sensor_list) == 0:
    log("No device file found!")
    error_log("No device file found!")
elif len(sensor_list) > 1:
    log("Device ambigouse!")
    error_log("Device ambigouse!")
else:
    log(f"Found device! {sensor_list[0]}")
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
        #wlan_ips = t_wlan(SSID,PASS,IP)
        wlan_ips = pico_wlan(SSID,PASS,IP)
        log("Device IP:",wlan_ips[0])
        break
    except Exception as e:
        blink(led)
        log(f"Network Error: {e}")
        error_log(f"Network Error: {e}")

if wlan_ips == '0.0.0.0':
    soft_reset()

led.off()

try:
    addr = socket.getaddrinfo(wlan_ips[0], 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(1)
    log('Socket listening on', addr)
except Exception as e:
    log(f"Socket Starting Error: {e}")
    error_log(f"Socket Starting Error: {e}")
    s.close()
    time.sleep(1)
    soft_reset()

# We start our one session to reconenct over and over again
sensor.measurement()
log("Ready for operation!")


while True:
    log("Waiting for client connection...")

    try:
        cl, addr = s.accept()
        log("Client connected:", addr)
        cl.settimeout(2)
    except OSError:
        continue

    # This timeout stops blocking our main loop and allows for reading datac
    last_measurement = utime.ticks_ms()

    while True:

        # Run the receiver
        try:            
            package = cl.recv(4096) # Extended this to 2048 to receive the large FastIC* cofig files
            rcv = package.decode('utf-8')
            print(f"Rcv.: {rcv}")
            if rcv == "":
                log("Terminated connection")
                cl.close()
                break
            #log("Received bytes:",rcv)

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
            elif "NULL_CONFIG" in rcv:
                config = open("lastconfig.txt","w")
                config.write("Sensorconfiglog")
                config.close()
                soft_reset()
            else:
                if sensor:
                    try:
                        response = sensor.server(rcv)
                    except Exception as e:
                        log(f"Sensor server failed! {e}")
                        error_log(f"Sensor server failed! {e}")
            print("--- RESPONSE --- ",response)
            if response != "INTERNAL":
                cl.send(response+'\r')
            if "TEST" not in rcv and response == "REPROGRAM":
                log("Restart!")
                reset()

        except OSError as e:

            if e.args[0] == 110:
                # This si timeou, this is ok!
                pass

            elif e.args[0] in (104, 9):
                log("Client disconnected")
                break

            else:
                log("Unexpected socket error:", e)
                break
        
        # Run our sensor to update the data
        if utime.ticks_diff(utime.ticks_ms(), last_measurement) > 500:
            sensor.measurement()
            last_measurement = utime.ticks_ms() 


        
    

