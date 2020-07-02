#!/bin/bash

# Source the aliases, functions, and environment variables

. /kwh/config/kwh.conf

W1DIR="/sys/bus/w1/devices"

# Exit if no one wire sensor exists   if [ ! -d $W1DIR ]    then    echo "There is no sensors!"exit 1    fi
DEVICES=$(ls $W1DIR)

# Output sting
OUTPUT=""

# Cycle across all founded sensors
for DEVICE in $DEVICES
do
# Ignore master
if [ $DEVICE != "w1_bus_master1" ]
then
    # Read sensor
    ANSWER=$(cat $W1DIR/$DEVICE/w1_slave)

    # Check answer and CRC; because if sensor disapear its address will be  9x00 but CRC will be valid
    echo -e "$ANSWER" | grep -e "00 00 00 00 00 00 00 00 00"  >&2
    if [ $? -ne 0 ]
    then
        # Temp is valid if CRC is valid
	echo -e "$ANSWER" | grep -q "YES"  >&2
	if [ $? -eq 0 ]
	then
	    # Temp is OK
	    # Get only temp from two line answer
	    TEMP=$(echo -e "$ANSWER" | grep "t=" | cut -f 2 -d "=")

	    INTEGER=$(($TEMP/1000)) # Integers
	    FRAC=$(($TEMP%1000)) # Decimals

	    # Handle minus frac! int (-1,0)°C
	    if [ "$FRAC" -lt "0" ] # Is rest minus?
            then
     	        FRAC=$(($FRAC * -1)) # Del minus
	        if [ "$INTEGER" -ge "0" ] # Is INTEGER 0 and more?
	        then
         	    INTEGER="-0" # This write minus to result, zero will be add next
	        fi
	    fi
	    # Handle one or two cyfer result - int (-1, 1)°C
	    if [ "$FRAC" -lt "100" ] # Is result less than  100?
	    then
	        if [ "$FRAC" -lt "10" ] # Is result less than 10?
	        then
	            FRAC="00"$FRAC # Add two zeros
	        else
	            FRAC="0"$FRAC # Add one zero
	        fi
	    fi

            sql="INSERT INTO kwh.data VALUES ($@, \"$DEVICE\",\"$INTEGER.$FRAC\");"
	    echo $sql | mysql -u pi

        else
	# CRC is invalid - error
	    echo "$DEVICE=CRC ERROR" >&2

   	fi
    fi
fi
done

