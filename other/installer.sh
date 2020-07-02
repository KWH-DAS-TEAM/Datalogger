#!/bin/bash

# Intro
echo ""
echo "================================================================================"
echo "=   Welcome to the KiloWatts for Humanity (KWH) Data Logger software package   ="
echo "================================================================================"
echo ""
echo "Thank you for your interest, and enjoy! Courtesy of KiloWatts for Humanity (KWH)"
echo ""
echo "This installer requires that the RPi be rebooted when complete"
echo "If you need to save any work, do not enter anything that starts with \"y\""
echo ""
echo "Would you like to continue with installation(y/n)?"
read ans
if [ "${ans:0:1}" != "y" ]; then
    echo ""
    echo "Exiting...Relaunch the installer.sh when you are ready."
    echo "Courtesy of KiloWatts for Humanity"
    echo ""
    exit
fi

# Install git for pulling the code from the repository
echo ""
echo "Verifying installation of and/or Installing git"
wait
sudo apt-get install -y git
status=$?
wait
if [ $status -ne 0 ]; then
    echo "unable to access git...aborting"
    echo "contact Dave@KiloWattsforHumanity.org for assistance"
fi

# Move to root and download data logger code from github
cd /
if [ ! -d "kwh" ]; then
  echo ""
  echo "Downloading data logger software to the root directory in /kwh"
  wait
  sudo git clone https://github.com/sbcdave/KWH kwh
  status=$?
  wait
  if [ $status -ne 0 ]; then
      echo ""
      echo "GitHub download stalled...rerun installer.sh"
      echo ""
      exit
  fi
fi

# MIGHT want to add a cd /kwh and git pull origin master here

# Create log directory
if [ ! -d /kwh/log ]; then
  mkdir /kwh/log
fi

# Download pigpio code from github
cd /kwh/lib
if [ ! -d pigpio ]; then
  echo ""
  echo "Downloading pigpio code to /kwh/lib"
  wait
  git clone https://github.com/joan2937/pigpio.git pigpio
  status=$?
  wait
  if [ $status -ne 0 ]; then
      echo ""
      echo "GitHub download stalled...rerun installer.sh"
      echo ""
      exit
  fi
fi

# MIGHT want to add a cd /kwh/lib/pigpio and git pull origin master here

# Change data logger code root directory owner:group to pi
echo ""
echo "Updating /kwh permissions"
wait
sudo chown -R pi:pi /kwh
wait

# Create symlink from /etc/defaults to kwh.conf file
echo ""
echo "Ensuring datalogger config is used at boot and setting auto-login to console"
wait
sudo ln -n /kwh/config/kwh.conf /etc/default/kwh.conf
wait
# Add kwh.conf file to root and pi's .bashrc
sudo cp /kwh/tmp/.bashrc /root/.bashrc
wait
cp /kwh/tmp/.bashrc /home/pi/.bashrc
wait
# Source the aliases functions and environment variables
. ~/.bashrc
wait
sudo cp /kwh/tmp/autologin@.service /etc/systemd/system/autologin@.service
wait
sudo systemctl daemon-reload
wait
sudo systemctl enable autologin@.service
wait

# Setting up SIM communications on ttyAMA0
echo ""
echo "Enabling ttyAMA0 on TX/RX for SIM comms"
wait
sudo systemctl mask serial-getty@ttyAMA0.service
wait

# Adjusting /boot/config.txt for SIM and Temp sensors communications
echo ""
echo "Updating /boot/config.txt to enable SIM and Temp sensor comms"
wait
sudo cp /kwh/tmp/config.txt /boot/config.txt
wait

# Enable simserver.service
echo ""
echo "Enabling sim server service"
sudo cp /kwh/tmp/simserver.service /etc/systemd/system/.
wait
sudo systemctl enable simserver.service
wait

# Enable pigpiod.service
echo ""
echo "Enabling pigpiod service"
sudo cp /kwh/tmp/pigpiod.service /etc/systemd/system/.
wait
sudo systemctl enable pigpiod.service
wait

# Enable gettime.service
echo ""
echo "Enabling get time service"
sudo cp /kwh/tmp/gettime.service /etc/systemd/system/.
wait
sudo systemctl enable gettime.service
wait

# Switching keyboard layout to US
echo ""
echo "Switching keyboard layout to US standard"
echo "Use \"sudo raspi-config\" if you would like to change it"
sudo cp /kwh/tmp/keyboard /etc/default/keyboard

# Activate 1 minute transmission via cron
echo ""
echo "Enabling cron jobs for reading sms, transmitting data, and updating the time"
wait
sudo cp /kwh/tmp/kwh.cron /etc/cron.d/.
wait
sudo chmod 644 /etc/cron.d/kwh.cron
wait

# NEED TO add echo output about the following commands
# Install dependencies
sudo apt-get install -y mysql-server mysql-client default-libmysqlclient-dev libusb-dev libusb-1.0-0-dev ppp at-spi2-core python3 python3-pip procmail
wait
sudo apt-get update
wait
sudo apt-get install -y mysql-server mysql-client default-libmysqlclient-dev libusb-dev libusb-1.0-0-dev ppp at-spi2-core python3 python3-pip procmail
wait
sudo pip3 install mysqlclient
wait
sudo pip3 install minimalmodbus

# Download sakis3g
cd /kwh/lib
if [ ! -d sakis3g ]; then
  git clone https://github.com/Trixarian/sakis3g-source.git sakis3g
fi

# Build sakis3g
sudo cp /usr/include/libusb-1.0/libusb.h /usr/include
wait
/kwh/lib/sakis3g/compile
wait
sudo cp /kwh/lib/sakis3g/build/sakis3gz /usr/bin/sakis3g
wait

# Build database structure
sudo mysql < /kwh/other/MySQL/kwh_db_structure.sql

# Disable GUI boot to lower power consumption and free up resources
sudo raspi-config nonint do_boot_behaviour B2

# NEED TO config setup here
# NEED TO investigate shutting down uneccesary services

# Reboot to finalize
echo ""
echo "Installation complete. We will soon reboot to enable communications with the PCB or other hardware solution."
echo ""
echo "If you would like KWH to host your data, please contact Dave@KiloWattsforHumanity.org"
echo "You can donate to KiloWatts for Humanity at http://kilowattsforhumanity.org"
echo "We hope you enjoy!"
echo ""
echo "Rebooting now is highly recommended as some communications will be erroring and filling log files"
echo "However, if you need to stop the reboot, you can use \"ctrl+c\" to kill the program without reboot"
echo "Press enter to reboot now..."
read ans
sudo shutdown -r now
