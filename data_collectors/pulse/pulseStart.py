#!/usr/bin/env python3
import subprocess
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')
# info on subprocess: https://docs.python.org/3/library/subprocess.html#converting-argument-sequence

# ***************************************************
#   THIS FILE IS GOING TO REPLACE pulseStart.sh ****
# ***************************************************

DB = KWH_MySQL.KWH_MySQL()
sql = "SELECT `key`, `value` FROM `config` WHERE `active`=1"

# constantly checking kwh environment variables from config table
# to turn on/turn off appropriate pulse channel
records = DB.SELECT(sql)
# dictionary of all key:value pair from config table
config_var = {}
for row in records:
    config_var[row[0]] = row[1]

pu01_running = False
pu02_running = False
pu03_running = False
pu04_running = False
pu05_running = False
pu06_running = False

# execute/stop the corresponding python file for each pulse channel
if config_var['PU01'] == '1':
    pu01 = subprocess.Popen('/kwh/data_collectors/pulse/PU01.py')
    pu01_running = True
else:
    if pu01_running == True:
        pu01.terminate()
        # pu01 HAS TO EXIST BEFOREHAND
        # => INITIALLY, CONFIG VALUES FOR ALL PULSE CHANNELS HAS TO BE 1

if config_var['PU02'] == '1':
    pu02 = subprocess.Popen('/kwh/data_collectors/pulse/PU02.py')
    pu02_running = True
else:
    if pu02_running == True:
        pu02.terminate()

if config_var['PU03'] == '1':
    pu03 = subprocess.Popen('/kwh/data_collectors/pulse/PU03.py')
    pu03_running = True
else:
    if pu03_running == True:
        pu03.terminate()

if config_var['PU04'] == '1':
    pu04 = subprocess.Popen('/kwh/data_collectors/pulse/PU04.py')
    pu04_running = True
else:
    if pu04_running == True:
        pu04.terminate()

if config_var['PU05'] == '1':
    pu05 = subprocess.Popen('/kwh/data_collectors/pulse/PU05.py')
    pu05_running = True
else:
    if pu05_running == True:
        pu05.terminate()

if config_var['PU06'] == '1':
    pu06 = subprocess.Popen('/kwh/data_collectors/pulse/PU06.py')
    pu06_running = True
else:
    if pu06_running == True:
        pu06.terminate()
