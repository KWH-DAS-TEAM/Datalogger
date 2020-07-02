#!/bin/bash

# Start pigpio daemon
sudo /usr/local/pigpio/util/pigpiod start

# Start all pulse listeners
/kwh/pulse/PU01.py &
/kwh/pulse/PU02.py &
/kwh/pulse/PU03.py &
/kwh/pulse/PU04.py &
/kwh/pulse/PU05.py &
/kwh/pulse/PU06.py &
/kwh/pulse/PU07.py &
/kwh/pulse/PU08.py &
