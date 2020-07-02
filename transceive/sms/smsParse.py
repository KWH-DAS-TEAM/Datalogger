#!/usr/bin/env python3

import re
import subprocess
import time

# Load environment variables
exec(open("/kwh/config/get_config.py").read())
DEBUG = int(config_var["DEBUG"])

if DEBUG:
    print("Running smsRead.sh")
p = subprocess.Popen("/kwh/transceive/sms/smsRead.sh")
# Wait for smsRead to complete
p.communicate()

if DEBUG:
    print("Running smsDelAll.sh")
p = subprocess.Popen("/kwh/transceive/sms/smsDelAll.sh")
p.communicate()

getMsgData = re.compile("\+CMGL:.*")

msgNum = 1

# THIS CODE HAS A BUG THAT IT WILL THROW AN EXCEPTION IF THERE IS NO
# MESSAGE TO READ. IT STILL WORKS, BUT IT WOULD BE NICE TO FIX THAT
# BUG

# Used to skip close on first temp file opening
tempOpen = False

time.sleep(1)

if DEBUG:
    print("Building files in msg/")
log = open("/kwh/transceive/sms/read.log", 'r+')
while True:
    line = log.readline()
    if not line:
        break
    if getMsgData.search(line):
        with open("/kwh/transceive/sms/msg/msg"+str(msgNum), 'w+') as temp:
            temp.write(line)
            line = log.readline()
            temp.write(line)

log.close()
# temp.close()

if DEBUG:
    print("Running smsProcess.py")
p = subprocess.Popen("/kwh/transceive/sms/smsProcess.py")
p.communicate()

if DEBUG:
    print("Running cleanMsg.sh")
p = subprocess.Popen("/kwh/transceive/sms/cleanMsg.sh")
p.communicate()
