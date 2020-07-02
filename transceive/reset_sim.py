#!/usr/bin/env python
import RPi.GPIO as gpio
from time import sleep
from sys import exit

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(12, gpio.OUT, initial=gpio.LOW)

gpio.output(12, gpio.HIGH)
sleep(1)
gpio.output(12, gpio.LOW)
