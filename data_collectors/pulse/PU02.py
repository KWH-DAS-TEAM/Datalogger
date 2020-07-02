#!/usr/bin/env python

# tally.py

import time

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

DIN = 20

pi.set_mode(DIN, pigpio.INPUT)
pi.set_pull_up_down(DIN, pigpio.PUD_DOWN)
pi.set_noise_filter(DIN, 200, 500)

pulse_cb = pi.callback(DIN, pigpio.RISING_EDGE)

while True:

    time.sleep(5)

    PU02 = open("/kwh/pulse/PU02", 'r')
    previous = int(PU02.read())
    PU02.close()

    new = pulse_cb.tally()
    current = previous + new
    PU02 = open("/kwh/pulse/PU02", 'w')
    PU02.write(str(current))
    PU02.close()
    pulse_cb.reset_tally()

pi.stop()
