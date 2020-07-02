#!/usr/bin/env python
import RPi.GPIO as pi
import signal
from time import sleep
from sys import exit
from sys import argv
from requests import get
from re import search

# load datalogger environment variables from config
execfile("/config/load_config.py")

channel = str(argv[1])
global count

pi.setmode(pi.BOARD)
pi.setup(32, pi.IN, pull_up_down=pi.PUD_DOWN)

def signal_handler(signal, frame):
        print('...closing PU'+channel)
        with open("/pulse/PU"+channel, 'w') as fd:
	        fd.write(str(count))
        exit(0)
	pi.remove_event_detect(32)
	sleep(1)
	pi.cleanup()

signal.signal(signal.SIGINT, signal_handler)
# investigate adding other signals

try:
	r=get("http://"+DOMAIN+":8080/render/?target="+STA+".PU"+channel+"&from=-2min&format=raw")
	s = search(r'.*\|(.*),(.*)',r.text)
	if s.group(2)=="None":
		if s.group(1)=="None":
			raise Exception('except')
		else:
			count=s.group(1)
	else:
		count=s.group(2)
except: 
	try:
		with open("/pulse/PU01", 'r') as fd:
			count=int(fd.read());
	except:
		count = 0

def counter(channel):
	global count 
	count += 1


pi.add_event_detect(32, pi.RISING, callback=counter, bouncetime=300)

while True:
	global count
	fd = open("/pulse/PU"+channel, 'w')
	fd.write(str(count))
	fd.close()
	sleep(1)
