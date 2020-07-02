#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 19

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU05 = open("/kwh/pulse/PU05", 'r')
previous = int(PU05.read())
PU05.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU05 = open("/kwh/pulse/PU05", 'w')
    PU05.write(str(current))
    PU05.close()

pi.stop()
