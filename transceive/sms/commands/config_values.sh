#!/bin/bash

. /kwh/config/kwh.conf

conf=$(config)

source /kwh/transceive/sms/smsSend.sh $1 `echo $conf`
wait

