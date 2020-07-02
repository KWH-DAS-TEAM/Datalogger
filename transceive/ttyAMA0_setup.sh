#!/bin/bash
stty -F /dev/ttyAMA0 `cat /kwh/config/sttySettings.tty`
