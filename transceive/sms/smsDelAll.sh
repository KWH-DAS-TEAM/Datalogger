#!/bin/bash

lock_file=/kwh/config/SIM_LOCK

. /kwh/config/kwh.conf

wait

# Load environment variables from config table
SIM_PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "SIM_PORT" AND active = 1' | mysql -u pi);
SIM_PORT=${SIM_PORT:6}

lockfile -1 -l 100 $lock_file
wait

echo AT+CMGF=1 | nc localhost $SIM_PORT \
	> /kwh/transceive/sms/delete.txt
wait
echo AT+CMGD=1,4 | nc localhost $SIM_PORT \
	>> /kwh/transceive/sms/delete.txt
wait

sudo rm -f $lock_file
wait
