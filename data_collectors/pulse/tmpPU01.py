#!/usr/bin/env python3

# tally.py

import pigpio
import time
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')
#import Bit_Bang_ADC

DB = KWH_MySQL.KWH_MySQL()

# load kwh environment variables from config
# exec(open("/kwh/config/load_config.py").read())
timestamp = sys.argv[0]

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 16

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU01 = open("/kwh/pulse/PU01", 'r')
previous = int(PU01.read())
PU01.close()

# selecting the last PU01 entry
#sql_select = "SELECT `value` FROM `data` WHERE `key`='PU01' ORDER BY time_created DESC LIMIT 1"
#records = DB.SELECT(sql_select)
# for row in records:
#    previous = row[0]

# print(previous)

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU01 = open("/kwh/pulse/PU01", 'w')
    PU01.write(str(current))
    PU01.close()
    print(current)

    # recheck config to see if it has to shut of , cannnot use load_config.py
    # if config['AD01'] == '1'
    # break out of while loop

    #sql_insert = "INSERT INTO `data` VALUES ("+timestamp+", 'PU01', "+str(current)+")"
    #result = DB.INSERT(sql_insert)

pi.stop()
