#!/bin/bash

lock_file=/kwh/config/SIM_LOCK

. /kwh/config/kwh.conf

wait

SIM_PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "SIM_PORT" AND active = 1' | mysql -u pi); 
SIM_PORT=${SIM_PORT:6}

lockfile -1 -l 100 $lock_file
wait

echo AT+CMGF=1 | nc localhost $SIM_PORT \
	> /kwh/transceive/sms/read.log
wait
echo AT+CMGL=\"ALL\" | nc localhost $SIM_PORT \
	>> /kwh/transceive/sms/read.log
wait
echo AT | nc localhost $SIM_PORT >> /kwh/transceive/sms/read.log

sudo rm -f $lock_file
wait
