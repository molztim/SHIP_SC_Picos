#Utillity platform

import network
import utime as time
import ubinascii

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

        print("\nConnected!",wlan.isconnected(),"\n")
    else:
        print("\nOld Connection continued!",wlan.isconnected(),"\n")
    
    wlan.ifconfig(adresses)
    return wlan.ifconfig()

def logsetting(rtc, contentlist):
    f = open("lastconfig.txt","a")
    now = rtc.datetime()
    head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
    body = ','.join(str(e) for e in contentlist)
    print(head,body)
    f.write("\n"+head+body)
    f.close()
    return None

from time import localtime as lt
def log(*service_string):
    output = "{:02d}:{:02d}:{:02d}|".format(*lt()[3:6])
    for i in service_string:
        output+= str(i)
    print(output)
    return None