#!/bin/bash

log="/kwh/log/transmit.log"

sudo systemctl stop simserver.service >> $log
wait

sudo /kwh/lib/sakis3g/sakis3g connect --console >> $log
wait

echo "Sleeping 5" >> $log
sleep 5
wait

sudo ntpd -q -g >> $log
wait

sudo /kwh/transceive/tcp/transmit.py >> $log
wait

sudo /kwh/lib/sakis3g/sakis3g disconnect --console >> $log
wait

sudo systemctl start simserver.service >> $log
wait
