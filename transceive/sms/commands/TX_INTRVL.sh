#!/bin/bash
# Command file for resetting the admin password

. /kwh/config/kwh.conf

STA=$(echo 'SELECT value FROM kwh.config WHERE `key` = "STA" AND active = 1' | mysql -u pi);
STA=${STA:6}

log=/kwh/transceive/sms/commands/TX_INTRVL.log

response="$STA - TX_INTRVL is now: $2"

/kwh/config/set_config.py TX_INTRVL $2
wait

echo "setconf TX_INTRVL $2" > $log

/kwh/transceive/sms/smsSend.sh $1 $response
wait

echo "Response sent to $1: $response" >> $log

echo `date` >> $log
