import network
import utime as time

wlan = network.WLAN(network.STA_IF)


def t_wlan(ssid, password, adresses):
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
