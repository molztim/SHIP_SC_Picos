import requests
import os
from datetime import datetime

#This code uses the http interface/query methode.
#There is a python library for InflixDB, but we prefere to use the http methode


#The bare minum you need to do before you can use this code:
#A) Fetch your lxplus username and password.
#B) Open a terminal. Execute: ssh -L 3000:194.12.159.165:3000 your_username_here@lxplus.cern.ch
#C) Enter your password when asked
#D) Keep this terminal alive!


host ="localhost"#"194.12.159.165"
#If you are at CERN, please use 194.12.159.165 instead of localhost!
port = 8086
token ="ACeJ_k8yw6RTS2mz6n9nvDdh8N3zcNd8_-xeEHpfxlzy66Eu1gq74MzDVjTTZQDFZL5mm-W1jyG9tjf7DYTRsg=="
#A quer example: query = "SELECT value FROM Pressure WHERE sensor='PRESS_B1' AND time > now()-5d;"


##################
#Build the Query #
##################

#This dict translates a quantity you may want to get (key) into what you need to querry from the influxdb.
#Please do not overgo this! Otherwise it will be an absolute mess to get the correct keys for influxdb
sensor_dict = {
    "LAB_pressure" : ["Pressure","PRESS_B1"],
    "LAB_level": ["Level","LEVEL_B1"],
    "environment_temperature" : ["Temperature","TEMP_E1"],
    "environment_pressure" : ["Pressure","PRES_E1"],
    "environment_humidity" : ["Humidity","HUM_E1"],
    "tilit_angle" : ["Rotation","RV_D1"],
    "vertical_position" : ["Distance","DIST_M1"],
    "horizontal_position" : ["Distance","DIST_M2"],
    "SIPM_VOUT_1" : ["voltage","VOUT_G1"],
    "SIPM_TEMP_1" : ["temperature","TEMP_G1"],
    "SIPM_VOUT_2" : ["voltage","VOUT_G2"],
    "SIPM_TEMP_2" : ["temperature","TEMP_G2"],
    "SIPM_VOUT_3" : ["voltage","VOUT_G3"],
    "SIPM_TEMP_3" : ["temperature","TEMP_G3"],
    "SIPM_VOUT_4" : ["voltage","VOUT_G4"],
    "SIPM_TEMP_4" : ["temperature","TEMP_G4"],
    "SIPM_VOUT_5" : ["voltage","VOUT_G5"],
    "SIPM_TEMP_5" : ["temperature","TEMP_G5"],
    "SIPM_VOUT_6" : ["voltage","VOUT_G6"],
    "SIPM_TEMP_6" : ["temperature","TEMP_G6"],
    "SIPM_VOUT_7" : ["voltage","VOUT_G7"],
    "SIPM_TEMP_7" : ["temperature","TEMP_G7"],
    "SIPM_VOUT_8" : ["voltage","VOUT_G8"],
    "SIPM_TEMP_8" : ["temperature","TEMP_G8"]
    

}

#From the dictionary above, please write the key in here which you wnat to get data
quantity_of_interest = "SIPM_VOUT_8"

operation = "value" # Define what sort of number you want. This just returns the values. Alternatives are mean(value), last(value)

topic = sensor_dict[quantity_of_interest][0] #The topic of the sensor. See MongoDb entry for topics or my list
sensor = sensor_dict[quantity_of_interest][1] #The sensor name

#Time code! Use only s,m,h,d,w to do a influxdb compatible query. InfluxDB is not build to use months and years! One can also use a timestamp with ns precision.
time = "> now()-12w" #A time argument

#This sets the entire query together. Please do not manipulate this
query = f"SELECT {operation} FROM {topic} WHERE sensor='{sensor}' AND time {time};"

print(f"\nCheck Query:\n{query}\n")

##################
#Finish    Query #
##################

params = {
    "db": "data",
    "org": "sbt",
    "q": query
}
headers = {
    "Authorization": f"Token {token}",
    "Accept": "application/csv"
}

#You will require this to get the http request
r = requests.get(f"http://{host}:{port}/query", params=params, headers=headers)
blob = r.content.decode()

#If your return is empty
if len(blob) == 0:
    raise RuntimeError("Return is empty!")

if "invalid" in blob:
    raise RuntimeError("WARNING: invalid return!",blob)

#This is no-compulsary. It extracts the values from the return and writes them into a list
lines = blob.split('\n')[:-1]
lines = [e.split(",") for e in lines]
values = [float(e[-1]) for e in lines[1:]]
time = [float(e[-2]) for e in lines[1:]]
print(f"header = {lines[0]}\n")

#print(lines) #-> Thisprint out all the data. Orders is always ['name', 'tags', 'time', 'value']
#Below it just prints the values
print(max(values),min(values),len(values))
