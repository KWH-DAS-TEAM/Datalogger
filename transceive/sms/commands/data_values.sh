#!/bin/bash

. /kwh/config/kwh.conf

STA=$(echo 'SELECT value FROM kwh.config WHERE `key` = "STA" AND active = 1' | mysql -u pi);
STA=${STA:6}

data="$STA $(data)"

source /kwh/transceive/sms/smsSend.sh $1 `echo $data`
wait

