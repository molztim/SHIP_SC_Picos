import socket
import time

devices = {
    #"laser2" : ["10.42.0.142","BLINK,NEW_DATA #-#beil.txt#-#\nBeil,RESTART_TEST 1430,ERROR_LOG,GET,SET_DIST X,SET_STAT X,SET_MODE X,SET_ORIENTATION X,GET"]
    "laser2" : ["10.42.0.142","BLINK"]
}
port = 80
clients = []
#Loop through items ind devices
for device in devices.values(): 
    content_string = ""
    clientX = socket.socket()
    clientX.settimeout(5)
    clientX.connect((device[0], 80))   
    clients.append(clientX)
    print(f"Successfull connection to {device[0]}!")

def send_rcv(client,message,name):
    client.send(message.encode())
    print(name, message)
    data = client.recv(1024).decode()
    print(data)
    time.sleep(0.2)
    return data

def send_cmd(client,message,name,cmd):
    client.send(cmd.encode())
    print(f"Send CMD {cmd} to {name}")
    print("New Configuration: ")
    send_rcv(client,message,name)

client = clients[0]

"""
for v in devices.values():
    for entries in v[1:]:
        local_config = [0]
        cmds = entries.split(",")
        for cmd in cmds:
            if "X" in cmd:
                cmd = cmd.replace("X",local_config[0])
                send_rcv(client,cmd,"laser2").split(",")
                local_config = local_config[1:]
            elif cmd != "GET":
                send_rcv(client,cmd,"laser2")
            else:
                local_config = send_rcv(client,cmd,"laser2")[:-1].split(",")
                del local_config[1]
                print(local_config)
            time.sleep(1)
"""
for i in range(2):
    send_rcv(client, "BLINK", "laser2")
    send_rcv(client, "ERROR_LOG", "laser2")
#send_rcv(client, "RESTART 281741\r", "laser2")
