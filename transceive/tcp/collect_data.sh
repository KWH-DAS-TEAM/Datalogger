#!/bin/bash

############################
# Run code to collect data #
############################


# Truncate data table to remove old redundant data that is already
# in the tx_string table
echo "truncate kwh.data" | mysql -u pi

# Start with timestamp to ensure all data points are linked in the 
# database via the minute they were collected
# Datetime stamp
dtm=`date +%s`
wait
echo "datetime: $?" >> /kwh/log/collect_data.log
echo "datetime: $?"

# Analog inputs
/kwh/data_collectors/analog.py $dtm
wait
echo "capture: $?" >> /kwh/log/collect_data.log
echo "capture: $?"

# One-Wire Temp sensors
/kwh/data_collectors/one-wire_bus.sh $dtm
wait
echo "one-wire: $?" >> /kwh/log/collect_data.log
echo "one-wire: $?"

# RPi Processor Temp
/kwh/data_collectors/rpi_temp.sh $dtm
wait
echo "rpi temp: $?" >> /kwh/log/collect_data.log
echo "rpi temp: $?"

# RPi Disk Use
/kwh/data_collectors/disk_space.sh $dtm
wait
echo "rpi disk: $?" >> /kwh/log/collect_data.log
echo "rpi disk: $?"

# Signal Quality
/kwh/data_collectors/signal_strength.sh $dtm
wait
echo "signal: $?" >> /kwh/log/collect_data.log
echo "signal: $?"

# ModBus
/kwh/data_collectors/modbus.py $dtm
wait
echo "modbus: $?" >> /kwh/log/collect_data.log
echo "modbus: $?"

###################################
# Build transmitable ASCII string #
###################################

/kwh/transceive/tcp/tx_string.py $dtm
# Decpricated by sakis3g
# echo $'\cZ' >> /kwh/transceive/tcp/tstring
wait
echo "tx_string: $?" >> /kwh/log/collect_data.log
echo "tx_string: $?"

#############################
# Initiate TCP transmission #
#############################

# Decpricated by sakis3g
#. /kwh/transceive/tcp/tcpSend.sh >> \
#/kwh/transceive/tcp/collect_data.log 2>&1
#wait
#echo "tcpSend: $?" >> /kwh/transceive/tcp/collect_data.log

#nc kwhstg.org 11001 < /kwh/transceive/tcp/tstring

#########################################
# Check for new SMS messages to process #
#########################################

# Moved due to switching to sakis3g
#/kwh/transceive/sms/smsParse.py >> /kwh/transceive/sms/smsParse.log
#wait
#echo "smsParse: $?" >> /kwh/transceive/tcp/collect_data.log

