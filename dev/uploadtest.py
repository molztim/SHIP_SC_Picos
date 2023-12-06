import socket

devices = {
    "test" : ["10.42.0.130","test1.py","test2.py"]
}
port = 80

#Start sending
print("Start Server...")

#Loop through items ind devices
for device in devices.values():
    #try:
    #    client = socket.socket()
    #    client.connect((device[0],port))
    #except:
    #    raise RuntimeError("No connection!")
    
    for file_name in device[1:]:
        file = open(file_name, 'r')
        content = file.read()
        content_string = f"#-#{file_name}#-#\n" + content
        print(content_string)
