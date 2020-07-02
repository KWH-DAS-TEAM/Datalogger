#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 13

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU06 = open("/kwh/pulse/PU06", 'r')
previous = int(PU06.read())
PU06.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU06 = open("/kwh/pulse/PU06", 'w')
    PU06.write(str(current))
    PU06.close()

pi.stop()
