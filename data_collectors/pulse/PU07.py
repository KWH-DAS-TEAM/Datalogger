#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 6

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU07 = open("/kwh/pulse/PU07", 'r')
previous = int(PU07.read())
PU07.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU07 = open("/kwh/pulse/PU07", 'w')
    PU07.write(str(current))
    PU07.close()

pi.stop()
