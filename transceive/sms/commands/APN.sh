#!/bin/bash

# Command file for resetting the admin password

. /kwh/config/kwh.conf

log=/kwh/transceive/sms/commands/APN.log

STA=$(echo 'SELECT value FROM kwh.config WHERE `key` = "STA" AND active = 1' | mysql -u pi); 
STA=${STA:6}

response="$STA - APN is now: $2"

setapn $2
echo "setapn $2" > $log
wait

/kwh/transceive/sms/smsSend.sh $1 $response
wait

echo "Response sent to $1: $response" >> $log

echo `date` >> $log
