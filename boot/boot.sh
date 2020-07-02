#!/bin/bash
# First steps at boot, before starting, simserver.service
# ensure the SIM_LOCK is gone for propper sim lock accessibility,
# kill the scheduler by removing the scheduler file, and ensure the wifi
# module is disabled to save on power.

# This allows us to ensure a reliable boot sequence and to launch
# the sim_server.py only after updating the time via sakis3g.

# Only after sim_server.py is started we re-enable the scheduler

# lock cleanup
date >> /kwh/log/boot.log
sudo rm /kwh/config/SIM_LOCK >> /kwh/log/boot.log
wait

# stop kwh scheduler
date >> /kwh/log/boot.log
sudo systemctl stop cron.service
sudo rm /var/spool/cron/crontabs/pi >> /kwh/log/boot.log
wait

# shutdown wifi module
date >> /kwh/log/boot.log
sudo ifconfig wlan0 down >> /kwh/log/boot.log
wait

# sleep to ensure all needed service are up before starting up sakis3g
# in the next step
date >> /kwh/log/boot.log
echo "Going to sleep" >> /kwh/log/boot.log
sleep 10
date >> /kwh/log/boot.log
echo "Sleep complete" >> /kwh/log/boot.log
wait

# start internet connection via sakis3g
date >> /kwh/log/boot.log
sudo /kwh/lib/sakis3g/sakis3g connect --console >> /kwh/log/boot.log
wait

# use three step ntp process to set time via RPi time service
date >> /kwh/log/boot.log
sudo ntpd -q -g >> /kwh/log/boot.log
wait

# shut off sakis3g connection
date >> /kwh/log/boot.log
sudo /kwh/lib/sakis3g/sakis3g disconnect --console >> /kwh/log/boot.log
wait

# start simserver.service
date >> /kwh/log/boot.log
sudo systemctl start simserver.service
echo "sim_server.py started in background" >> /kwh/log/boot.log

# re-implement the scheduler
date >> /kwh/log/boot.log
sudo cp /kwh/boot/kwh_scheduler.cron /var/spool/cron/crontabs/pi >> /kwh/log/boot.log
sudo chmod 600 /var/spool/cron/crontabs/pi >> /kwh/log/boot.log
sudo systemctl start cron.service
