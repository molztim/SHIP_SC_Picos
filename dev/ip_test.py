import ipaddress

print(ipaddress.ip_network('192.168.0.0/24'))
var = ipaddress.ip_address('192.168.0.1') in ipaddress.ip_network('192.168.0.0/24') #Basicly comapre if IP of device is in network IP
print(var)
