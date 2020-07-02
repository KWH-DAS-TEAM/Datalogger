#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 16

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU01 = open("/kwh/data_collectors/pulse/PU01", 'r')
previous = int(PU01.read())
PU01.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU01 = open("/kwh/data_collectors/pulse/PU01", 'w')
    PU01.write(str(current))
    PU01.close()

pi.stop()
