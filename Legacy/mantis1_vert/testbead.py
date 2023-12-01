from time import localtime as lt
from machine import RTC

rtc = RTC()

f = open("lastconfig.txt","a")
lines = f.read()
f.close()
contentlist = [int(e) for e in lines.split("\n")[-1].split("|")[-1].split(",")]
calib,laserstatus,lastdata,fast = contentlist
print(contentlist)


contentlist = [0,1,20.0,0]

f = open("lastconfig.txt","a")
now = rtc.datetime()
head = "{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6])
body = ','.join(str(int(e)) for e in contentlist)
print(head,body)
f.write("\n"+head+body)
f.close()

#now = rtc.datetime()
#print("{:02d}.{:02d}.{:02d}-{:02d}:{:02d}:{:02d}|".format(now[2],now[1],now[0],now[4],now[5],now[6]))