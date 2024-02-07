import socket
import time
from datetime import datetime

clients = []
ips = [111,112,113,114,115,116,117,100,101,102,103,104,105,106,107,108,109,110,125,126,127,128,129,130,131,132,140,141,142,143,144,145]

ips_all = {
    "t1" : (100,"PING"),
    "t2" : (101,"PING"),
    "t3" : (102,"PING"),
    "t4" : (103,"PING"),
    "t5" : (104,"PING"),
    "t6" : (105,"PING"),
    "t7" : (106,"PING"),
    "t8" : (107,"PING"),
    "t9" : (108,"PING"),
    "t10" : (109,"PING"),
    "t11" : (110,"PING"),
    "t12" : (111,"PING"),
    "t13" : (112,"PING"),
    "t14" : (113,"PING"),
    "t15" : (114,"PING"),
    "t16" : (115,"PING"),
    "t17" : (116,"PING"),
    "t18" : (117,"PING"),
    "gw1" : (125,"GET_VOUT"),
    "gw2" : (126,"GET_VOUT"),
    "gw3" : (127,"GET_VOUT"),
    "gw4" : (128,"GET_VOUT"),
    "gw5" : (129,"GET_VOUT"),
    "gw6" : (130,"GET_VOUT"),
    "gw7" : (131,"GET_VOUT"),
    "gw8" : (132,"GET_VOUT"),
    "spider" : (140,"GET_HDIST"),
    "dragonfly" : (141,"GET_ANGLE"),
    "laser1" : (142,"GET_DIST"),
    "laser2" : (143,"GET_DIST"),
    "env" : (144,"GET_TEMP"),
    "beetle" : (145,"GET_PRES")
}

ips_cern = {
    "gw1" : (125,"GET_VOUT"),
    "gw2" : (126,"GET_VOUT"),
    "gw3" : (127,"GET_VOUT"),
    "gw4" : (128,"GET_VOUT"),
    "gw5" : (129,"GET_VOUT"),
    "gw6" : (130,"GET_VOUT"),
    "gw7" : (131,"GET_VOUT"),
    "gw8" : (132,"GET_VOUT"),
    "spider" : (140,"GET_HDIST"),
    "dragonfly" : (141,"GET_ANGLE"),
    "laser1" : (142,"GET_DIST"),
    "laser2" : (143,"GET_DIST"),
    "env" : (144,"GET_TEMP"),
    "beetle" : (145,"GET_PRES")
}

ip_test = {
    "laser1" : (142,"GET_DIST"),
    }

ips = ip_test

for key,value in ips.items():
    ip = value[0]
    print(f"Attempt connection to: {key} - {ip} - ", end="")
    try:
        clientX = socket.socket()
        clientX.settimeout(1)
        clientX.connect(('10.42.0.'+str(ip), 80))
        print("Successfull!")
        clients.append([clientX, value[1], key])
    except:
        print("Failure!")

if len(clients) == 0:
    raise RuntimeError("No device connected!")

print("--Total connected clients: ",len(clients),"--")

def send_rcv(client,message,name):
    client.send(message.encode())
    data = client.recv(1024).decode()
    print(name,message,data)
    time.sleep(0.2)
    return None

def send_cmd(client,message,name,cmd):
    client.send(cmd.encode())
    print(f"Send CMD {cmd} to {name}")
    print("New Configuration: ")
    send_rcv(client,message,name)


i = 0
start = datetime.now()



try:

    for j in range(4):
        for i in range(10):
            i = i+1
            print(f"#{i}")
            now = datetime.now() - start
            print(now)
            for connections in clients:
                send_rcv(*connections)
            time.sleep(1)


except Exception as e:
    print(e)
    for connections in clients:
        connections[0].close()
    print("Terminate Connection\n") 
       
