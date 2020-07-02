#!/bin/bash

lock_file=/kwh/config/SIM_LOCK

. /KWH/config/kwh.conf

lockfile -1 -l 100 $lock_file
wait

pulse_config=$( 
#SIM_PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "SIM_PORT" AND active = 1' | mysql -u pi); 
#SIM_PORT=${SIM_PORT:6}

#echo AT+CSQ | nc localhost $SIM_PORT > /kwh/log/signal_strength.log
#wait
#sq=$(grep '\+CSQ:' /kwh/log/signal_strength.log | sed -E 's/\+CSQ: ([0-9]*),.*/\1/')
#wait
#sql="INSERT INTO kwh.data VALUES ($@,\"SQ\",$sq)"
#echo $sql | mysql -u pi

sudo rm -f $lock_file
wait

# Start pigpio daemon
sudo /usr/local/pigpio/util/pigpiod start

# Start all pulse listeners
/kwh/pulse/PU01.py &
/kwh/pulse/PU02.py &
/kwh/pulse/PU03.py &
/kwh/pulse/PU04.py &
/kwh/pulse/PU05.py &
/kwh/pulse/PU06.py &
/kwh/pulse/PU07.py &
/kwh/pulse/PU08.py &

