#!/usr/bin/env python
import pigpio
import signal
from sys import exit
from requests import get
from re import match

# load datalogger environment variables from config
execfile("/config/load_config.py")

def signal_handler(signal, frame):
        print('...closing PU01')
        with open("/pulse/PU01", 'w') as PU01
	        PU01.write(str(count))
        exit(0)
signal.signal(signal.SIGINT, signal_handler)

# NEED to build config logic for pulse channels and get this working again
try:
	r=get("http://"+DOMAIN+":8080/render/?target="+STA+".PU01.Total_Energy&from=-2min&format=raw")
	mObj = match( r'.*60\|(.*).0,(.*)',r.text,flags=0)
	print mObj.group(1)
	print mObj.group(2)
	if mObj.group(2)="None":
		count=mObj.group(1)
	else:
		count=mObj.group(2)
except: 
	try:
		PU01=open("/pulse/PU01", 'r')
	except:
		PU01=open("/pulse/PU01", 'w+')
	
	count=int(PU01.read());

PU01.close()

pi=pigpio.pi()
pi.set_mode(26, pigpio.INPUT)
pi.set_pull_up_down(12, pigpio.PUD_DOWN)

while True:
	if pi.wait_for_edge(12):
		pi.wait_for_edge(12)
		count+=1
		PU01=open("/pulse/PU01", 'w')
		PU01.write(str(count))
		PU01.close()
