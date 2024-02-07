import socket
import time

devices = {
    "test" : ["10.42.0.142","fey_testdevice/test_device.py"]
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

for client in clients:
    print("Fetch for Error_log...")
    client.send("ERROR_LOG".encode())
    print("I got an answer!")
    log = client.recv(1024).decode()
    print(log)
