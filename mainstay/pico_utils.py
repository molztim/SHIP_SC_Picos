#Utillity platform
import os
import network
import utime as time
import ubinascii
from time import localtime as lt

def t_wlan(ssid, password, adresses):
    wlan = network.WLAN(network.STA_IF)
    if wlan.status() != network.STAT_GOT_IP: 
        wlan.active(True)
        wlan.connect(ssid, password)
        time.sleep_ms(1000)
        while wlan.status() != network.STAT_GOT_IP:
            if wlan.status() == network.STAT_CONNECTING:
                print(".",end="")
            else:
                if wlan.status() == network.STAT_WRONG_PASSWORD:
                    raise RuntimeError('Wrong Password!')
                elif wlan.status() == network.STAT_NO_AP_FOUND:
                    raise RuntimeError('No Access Point Responding! Check SSID.')
                elif wlan.status() == network.STAT_CONNECT_FAIL:
                    raise RuntimeError("No f*cking idea!")
                else:
                    #raise RuntimeError("Oh shit, not gud")
                    print(".",end="")
            time.sleep_ms(1000)

        log("Connected!",wlan.isconnected())
    else:
        log("Old Connection continued!",wlan.isconnected())
    
    wlan.ifconfig(adresses)
    return wlan.ifconfig()

def config_writer(rtc, contentlist):
    f = open("lastconfig.txt","a")
    now = rtc.datetime()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    body = ','.join(str(e) for e in contentlist)
    log("Write Config "+head+body)
    f.write("\n"+head+body)
    f.close()
    return None

def config_reader():
    f = open("lastconfig.txt","a")
    lines = f.read()
    f.close()
    contentlist = [int(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
    return contentlist


def log(*service_string):
    output = "{:02d}:{:02d}:{:02d}|".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None

def error_log(string):
    now = lt()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    output = head +string
    f = open("error_log.txt","a")
    f.write("\n"+output)
    f.close()
    return None

def rcv_new_file(rcv):
    try:
        #Receive the package as one
        rcv = rcv[9:]
        print("Received data: ",rcv[:25],"...")
        buffer = open("new_software_buffer.txt","a")
        buffer.write(rcv)
        buffer.close()
        time.sleep(0.1)
        log(f'{len(rcv)} an Zeilen wurde geschrieben')

    except Exception as e:
        log(f"Error: {e} occured when appending the new data to the buffer file!")


def reprogramm(rcv):

    checksum = int(rcv.split(" ")[1])
    file = open("new_software_buffer.txt","r")
    new_software = file.read()
    file.close()
    internal_checksum = sum(ord(char) for char in new_software)
    log(f"Checksum of internal file {internal_checksum}, rcv. checksum: {checksum}")
    if checksum != internal_checksum:
        log("Checksums do NOT match! Error in Transmission")
        error_log("Checksums do NOT match! Error in Transmission")
        buffer = open("new_software_buffer.txt","w")
        buffer.close()
        return "SUMERROR"

    log("Done!")
    
    #Split the receive in file names and content
    splitsymbol = "".join(["#","-","#"])
    parts = new_software.split(splitsymbol)
    names = parts[1::2]
    content = parts[2::2]
    log("Names: ",names)

    #Create new files from file names and content
    for name, data in zip(names,content):
        #pint(f"Name: {name} , {data}")
        log(f"Write File {name} with {len(data)} worth of data...")
        file = open(name, 'w')
        file.write(data)
        file.close()
    new_mem = os.listdir()
    for entry in names:
        if entry in new_mem: log(f"{entry} was written!")
        else: log(f"{entry} not found!")

    #Clear buffer
    buffer = open("new_software_buffer.txt","w")
    buffer.close()
    return "REPROGRAM"

def fetch_errorlog():
    log("Fetching Error log")
    log_file = open("error_log.txt").read()
    return log_file

def blink(led,count=1):
        led.off()
        for i in range(count):
            led.toggle()
            time.sleep_ms(100)
            led.toggle()
            time.sleep_ms(400)
        led.off()

def blank():
    log("Erase old Software buffer")
    buffer = open("new_software_buffer.txt","w")
    buffer.close()
    return "INTERNAL"
