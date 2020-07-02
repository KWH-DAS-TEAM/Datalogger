#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 26

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU04 = open("/kwh/pulse/PU04", 'r')
previous = int(PU04.read())
PU04.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU04 = open("/kwh/pulse/PU04", 'w')
    PU04.write(str(current))
    PU04.close()

pi.stop()
