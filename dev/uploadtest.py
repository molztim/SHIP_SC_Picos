import socket
import time
import os 
import datetime

def upload(paths, client): #This system uses a list of paths!
    client.send(("NEW_SOFTWARE").encode())
    content_string = ""
    date = datetime.datetime.now().strftime("%c")
    for file_path in paths:
        file = open(file_path, 'r')
        content = file.read()
        file_name = file_path.split("/")[-1]
        content_string = content_string + f"#-#{file_name}#-##{date}\n" + content
        file.close
    
    checksum =  sum(ord(char) for char in content_string)
    cut_string = [content_string[i:i+750] for i in range(0,len(content_string), 750)]

    print("Sending: ",len(cut_string))

    i = 0
    for snippet in cut_string:
        i=i+1
        print(f"Send Snipped #{i}/{len(cut_string)}")
        client.send(("NEW_DATA "+snippet).encode())
        time.sleep(1)

    time.sleep(1)
    print(f"Send RESTART {checksum}")
    client.send(f"RESTART {checksum}".encode())
    data = client.recv(1024).decode()

    return data
port = 80

"""
devices = {
    "test" : ["10.42.0.142","laser2/main.py","laser2/new_software_buffer.txt","laser2/laserrangefinder.py","laser2/laser_device.py","laser2/error_log.txt","laser2/pico_ultis.py","laser2/lastconfig.txt"]
}

#Loop through items ind devices
for device in devices.values(): 
    clientX = socket.socket()
    clientX.settimeout(5)
    clientX.connect((device[0], 80))   
    print(f"Successfull connection to {device[0]}!")
    print(device[1:])
    upload(device[1:],clientX)
    print("Finished!")

    #clientX.close()
"""
devices = {
    "test" : ["10.42.0.142","laser2"]
}

print(os.listdir('laser2'))

#Loop through items in devices
for device in devices.values(): 
    clientX = socket.socket()
    clientX.settimeout(5)
    clientX.connect((device[0], 80))   
    print(f"Successfull connection to {device[0]}!")
    path = device[1]
    liste = [f"{path}/"+file for file in os.listdir(path)]
    upload(liste,clientX)
    print("Finished!")
    clientX.close()
