#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 5

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

PU08 = open("/kwh/pulse/PU08", 'r')
previous = int(PU08.read())
PU08.close()

while True:

    time.sleep(5)

    new = pulse_cb.tally()
    current = previous + new
    PU08 = open("/kwh/pulse/PU08", 'w')
    PU08.write(str(current))
    PU08.close()

pi.stop()
