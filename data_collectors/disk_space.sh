#!/bin/bash

# Collect disk memory use data via df command
mem_array=(`df /`)
mem_free=${mem_array[-3]}
percent_used=${mem_array[-2]}
# Removing the trailing %
percent_used=${percent_used::-1}

sql='INSERT INTO kwh.data VALUES ('$@',"DISK",'$mem_free'.'$percent_used');'
echo $sql | mysql -u pi
