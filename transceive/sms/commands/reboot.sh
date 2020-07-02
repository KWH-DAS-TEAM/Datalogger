#!/bin/bash

# Command file for resetting the admin password

. /kwh/config/kwh.conf

STA=$(echo 'SELECT value FROM kwh.config WHERE `key` = "STA" AND active = 1' | mysql -u pi);
STA=${STA:6}

log=/kwh/transceive/sms/commands/reboot.log

response="$STA is rebooting"

echo "Rebooting via SMS" > $log

/kwh/transceive/sms/smsSend.sh $1 $response
wait

echo "Response sent to $1: $response" >> $log 

echo `date` >> $log

/kwh/transceive/sms/commands/reboot_in_10s.sh &
