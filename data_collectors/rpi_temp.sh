#!/bin/bash
temp=`/opt/vc/bin/vcgencmd measure_temp`
temp=${temp:5}
temp=${temp::-2}
sql='INSERT INTO kwh.data VALUES ('$@',"PPT",'$temp');'
echo $sql | mysql -u pi
