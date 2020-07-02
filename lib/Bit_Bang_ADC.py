#!/usr/bin/env python
import RPi.GPIO as GPIO


def readadc(adcnum):

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    CLK = 18
    MISO = 23
    MOSI = 24
    CS = 25

    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)

    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(CS, True)

    GPIO.output(CLK, False)  # start clock low
    GPIO.output(CS, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(MOSI, True)
        else:
            GPIO.output(MOSI, False)
        commandout <<= 1
        GPIO.output(CLK, True)
        GPIO.output(CLK, False)

    adcout = 0
    # read in one empty bit, one null bit and 12 ADC bits
    for i in range(14):
        GPIO.output(CLK, True)
        GPIO.output(CLK, False)
        adcout <<= 1
        if (GPIO.input(MISO)):
            adcout |= 0x1

    GPIO.output(CS, True)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout
