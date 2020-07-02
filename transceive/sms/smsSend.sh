#!/bin/bash

lock_file=/kwh/config/SIM_LOCK

# Explain usage
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: sendsms <phone number> <message>";
    exit 0;
fi

. /kwh/config/kwh.conf

log="/kwh/transceive/sms/smsSend.log"
wait

SIM_PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "SIM_PORT" AND active = 1' | mysql -u pi); 
SIM_PORT=${SIM_PORT:6}
PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "PORT" AND active = 1' | mysql -u pi); 
PORT=${PORT:6}
DOMAIN=$(echo 'SELECT value FROM kwh.config WHERE `key` = "DOMAIN" AND active = 1' | mysql -u pi); 
DOMAIN=${DOMAIN:6}
APN=$(echo 'SELECT value FROM kwh.config WHERE `key` = "APN" AND active = 1' | mysql -u pi); 
APN=${APN:6}

# Wait for lock
lockfile -1 -l 100 $lock_file
wait

# Prep SIM800 for SMS
echo AT+CMGF=1 | nc localhost $SIM_PORT > $log
wait

# Start message to input phone number
echo AT+CMGS=\"$1\" | nc localhost $SIM_PORT >> $log
wait

# Input message
echo -n ${@: -`expr $# - 1`} | nc localhost $SIM_PORT >> $log
wait

# Send message
echo $'\cZ' | nc localhost $SIM_PORT >> $log
wait

# Return lock
sudo rm -f $lock_file
wait
