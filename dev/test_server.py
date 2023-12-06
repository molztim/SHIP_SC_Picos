import socket
from time import sleep

IPs = {
    "test" : '10.42.0.131'
}
port = 80

print("Start Server...")
try:
    client = socket.socket()
    client.connect((IPs["test"],port))
except:
    raise RuntimeError("No connection!")

print("Connected, sending...")
while True:
    try:
        message = "GET_DUMMY\r"
        client.send(message.encode())
        data = client.recv(1024).decode()
        print(f"Received: {data}")
        sleep(1)
    except:
        client.close()
        print("Terminate Connection\n")