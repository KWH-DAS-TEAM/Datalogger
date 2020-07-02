#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 21

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU03 = open("/kwh/pulse/PU03", 'r')
previous = int(PU03.read())
PU03.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU03 = open("/kwh/pulse/PU03", 'w')
    PU03.write(str(current))
    PU03.close()

pi.stop()
