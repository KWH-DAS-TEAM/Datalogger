#!/bin/bash
echo 'SELECT * FROM kwh.tx_string WHERE `timestamp` like "'$@'%"' | mysql -u pi
