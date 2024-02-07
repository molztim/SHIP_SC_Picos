import subprocess
import time
import datetime

cmd_on = "sudo nmcli r wifi on".split(" ")
cmd_hotspot = "sudo nmcli device wifi hotspot".split(" ")


while True:
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = subprocess.check_output(["nmcli", "dev"], universal_newlines=True)
    lines = output.split("\n")
    for line in lines:
        if all(word in line for word in ["wifi", "connected", "Hotspot"]):
            print(f"{date} Hotspot active for {line.split(chr(32))[0]}")
            time.sleep(15)

        elif all(word in line for word in ["wifi", "unavailable"]):
            print(f"{date} Wifi off for {line.split(chr(32))[0]}")
            subprocess.run(cmd_on,input="2200_enterPrise\n".encode())
            time.sleep(1)

        elif all(word in line for word in ["wifi", "disconnected"]):
            print(f"{date} Hotspot off for {line.split(chr(32))[0]}")
            subprocess.run(cmd_hotspot,input="2200_enterPrise\n".encode())
            time.sleep(1)

    time.sleep(1)
