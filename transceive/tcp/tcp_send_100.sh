#!/bin/bash
lock_file=/kwh/config/SIM_LOCK

. /kwh/config/kwh.conf

log="/kwh/log/tcp_send.log"
wait

SIM_PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "SIM_PORT" AND active = 1' | mysql -u pi); 
SIM_PORT=${SIM_PORT:6}
PORT=$(echo 'SELECT value FROM kwh.config WHERE `key` = "PORT" AND active = 1' | mysql -u pi); 
PORT=${PORT:6}
DOMAIN=$(echo 'SELECT value FROM kwh.config WHERE `key` = "DOMAIN" AND active = 1' | mysql -u pi); 
DOMAIN=${DOMAIN:6}
APN=$(echo 'SELECT value FROM kwh.config WHERE `key` = "APN" AND active = 1' | mysql -u pi); 
APN=${APN:6}
COMPRESS=$(echo 'SELECT value FROM kwh.config WHERE `key` = "COMPRESS" AND active = 1' | mysql -u pi);
COMPRESS=${COMPRESS:6}

# Wait for lock
lockfile -1 -l 100 $lock_file
wait

# Collect tx_string from the database
first="TRUE"
echo 'SELECT tx_string FROM kwh.tx_string LIMIT 100;' | mysql -u pi | while read record
do
    if [ "$first" = "TRUE" ]; then
      echo "discarding first token...column name"
      read record
      first="FALSE"
    fi
    wait

    if [ $COMPRESS -eq 1 ]; then
        tx_string=$(/kwh/transceive/tcp/compress.py $(echo $record))
	echo "compressed: $tx_string"
    else
        tx_string=$record
	echo "not compressed: $tx_string"
    fi
    wait

    # Send data to server
    echo AT+CMEE=2 | nc localhost $SIM_PORT > $log
    wait
    echo AT+CIPSHUT | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CGATT=0 | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CGATT=1 | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPSHUT | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPMUX=0 | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CSTT=\"$APN\" | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIICR | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIFSR | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPSTART=\"TCP\",\"$DOMAIN\",\"$PORT\" \
    	| nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPSEND | nc localhost $SIM_PORT >> $log
    wait
    echo $tx_string | nc localhost $SIM_PORT >> $log
    wait
    echo $'\cZ' | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPCLOSE | nc localhost $SIM_PORT >> $log
    wait
    echo AT+CIPSHUT | nc localhost $SIM_PORT >> $log
    wait

done
# Return lock
sudo rm -f $lock_file
wait
