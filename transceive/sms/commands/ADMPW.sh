#!/bin/bash
# Command file for resetting the admin password

. /kwh/config/kwh.conf

STA=$(echo 'SELECT value FROM kwh.config WHERE `key` = "STA" AND active = 1' | mysql -u pi);
STA=${STA:6}

response="$STA - Admin password is now: $2"

/kwh/config/set_config.py ADMPW $2
wait

echo "setconf ADMPW $2" > /kwh/transceive/sms/commands/ADMPW.log

/kwh/transceive/sms/smsSend.sh $1 $response
wait

echo "Response sent to $1: $response" >> /kwh/transceive/sms/commands/ADMPW.log

echo `date` >> /kwh/transceive/sms/commands/ADMPW.log
