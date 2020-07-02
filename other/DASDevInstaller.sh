#!/bin/bash

# Intro
echo ""
echo "================================================================================"
echo "=   Welcome to the KiloWatts for Humanity (kwh) Data Logger software package   ="
echo "================================================================================"
echo ""
echo "Thank you for being a part of the kwh DAS team!"
echo ""
echo "This installer is broken into steps to help you relaunch it at a certain point"
echo "in case of failure during the script. To jump to a step, re-execute the"
echo "installer and pass the step number in as a parameter."
echo "e.g. ./DASDevInstaller.sh 5"
if [[ ! "$1" =~ .+ ]]; then
echo ""
echo "This installer requires that the RPi be rebooted when complete"
echo "If you need to save any work, do not answer anything that starts with \"y\""
echo ""
echo "Would you like to continue with installation(y/n)?"
read ans
if [ "${ans:0:1}" != "y" ]; then
    echo ""
    echo "Exiting...Relaunch the DASDevInstaller.sh when you are ready."
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
    echo "Unable to install git...aborting"
    echo "contact dave@KiloWattsforHumanity.org for assistance"
fi
# Install procmail for lockfile
echo ""
echo "Installing procmail for its lockfile program"
wait
sudo apt-get install -y procmail
status=$?
wait
if [ $status -ne 0 ]; then
    echo "Unable to install procmail...aborting"
    echo "contact dave@KiloWattsforHumanity.org for assistance"
fi
# Install minimalmodbus for modbus
echo ""
echo "Installing minimalmodbus"
wait
sudo pip install -U minimalmodbus
status=$?
wait
if [ $status -ne 0 ]; then
    echo "Unable to install minimalmodbus...aborting"
    echo "contact dave@KiloWattsforHumanity.org for assistance"
fi
fi

# Step (1)
if [[ ! "$1" =~ .+ ]] || [ "$1" = "1" ]; then
# Move to root and download data logger code from github
cd /
echo ""
echo "Step (1)"
echo "Downloading data logger software to the root directory in /kwh"
echo "Credit: kwh DAS Team and Seattle University Senior Design Team ECE 18.5"
wait
sudo git clone https://github.com/sbcdave/kwh.git
status=$?
wait
if [ $status -ne 0 ]; then
    echo ""
    echo "GitHub download stalled...rerun ./DASDevInstaller.sh 1"
    echo ""
    exit
fi
fi

# Step (2)
if [[ ! "$1" =~ .+ ]] || [ "$1" = "1" ] || [ "$1" = "2" ]; then
# Download pigpio code from github
cd /
echo ""
echo "Step (2)"
echo "Downloading pigpio code to /usr/local/pigpio"
echo "Credit: GitHub - joan2937"
wait
cd /usr/local
if [ ! -d pigpio ]; then
    sudo git clone https://github.com/joan2937/pigpio.git
    status=$?
    wait
    if [ $status -ne 0 ]; then
        echo ""
        echo "GitHub download stalled...rerun ./DASDevInstaller.sh 2"
        echo ""
        exit
    fi
fi

# Change data logger code root directory owner:group to pi
echo ""
echo "Updating /kwh permissions"
wait
sudo chown -R pi:pi /kwh
wait

# Shut down unnecessary services
#echo ""
#echo "Shutting down unnecessary services"
#echo "Apache2..."
#sudo systemctl disable apache2

# Create symlink from /etc/defaults to kwh.conf file
echo ""
echo "Ensuring data logger config is used at boot and setting auto-login"
wait
sudo ln -n /kwh/config.conf /etc/default.conf
wait
# Add kwh.conf file to root and pi's .bashrc
sudo cp /kwh/moves/.bashrc /root/.bashrc
wait
cp /kwh/moves/.bashrc /home/pi/.bashrc
wait
# Source the aliases, functions, and environment variables
. ~/.bashrc
wait
sudo cp /kwh/moves/autologin@.service /etc/systemd/system/autologin@.service
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
sudo cp /kwh/moves/config.txt /boot/config.txt
wait

# Enable simserver.service
echo ""
echo "Enabling sim server service"
sudo cp /kwh/moves/simserver.service /etc/systemd/system/.
wait
sudo systemctl enable simserver.service
wait

# Enable data logger service
echo ""
echo "Enabling dlogger service for pigpiod, pulse counting, and updating the time at boot"
sudo cp /kwh/moves/dlogger /etc/init.d/.
wait
sudo update-rc.d dlogger defaults
wait
sudo systemctl daemon-reload

# Switching keyboard layout to US
echo ""
echo "Switching keyboard layout to US standard"
echo "Use \"sudo raspi-config\" or edit /etc/default/keyboard"
echo "if you would like to change it"
sudo cp /kwh/moves/keyboard /etc/default/keyboard
fi

# Step (3)
if [[ ! "$1" =~ .+ ]] || [ "$1" = "1" ] || [ "$1" = "2" ] || [ "$1" = "3" ]; then
echo ""
echo "Installing hub to simplify DAS development via GitHub"
echo "Credit: https://github.com/github/hub.git"

cd /kwh

if [ ! -f go1.10.2.linux-armv6l.tar.gz ] && [ ! -d /usr/local/go ]; then
    echo ""
    echo "Downloading GoLang for hub build"
    echo "Credit: Google"
    echo ""
    wget https://dl.google.com/go/go1.10.2.linux-armv6l.tar.gz;
    status=$?
fi
wait
if [ $status -ne 0 ]; then
    echo "GoLang download stalled...if there is a partial download file in /kwh"
    echo "(e.g. /kwh/go1.10.2.linux-armv6l.*) delete it with rm"
    echo "Then rerun ./DASDevInstaller.sh 3"
    exit
fi

if [ ! -d /usr/local/go ]; then
    echo "Unpacking Go to /usr/local/go...";
    sudo tar -C /usr/local -xzf /kwh/go1.10.2.linux-armv6l.tar.gz;
fi
wait

echo ""
echo "Moving Go binary to a location that is in \$PATH"
sudo cp /usr/local/go/bin/go /usr/sbin/go
wait

echo ""
echo "Deleting Go tar.gz"
rm /kwh/go1.10.2.linux-armv6l.tar.gz
wait
fi

# Step (4)
if [[ ! "$1" =~ .+ ]] || [ "$1" = "1" ] || [ "$1" = "2" ] || [ "$1" = "3" ] || [ "$1" = "4" ]; then
echo ""
echo "Downloading hub into /usr/local ..."
cd /usr/local
wait
sudo git clone https://github.com/github/hub.git
status=$?
wait
if [ $status -ne 0 ]; then
    echo "GitHub download stalled...rerun ./DASDevInstaller.sh 4"
    exit
fi

echo ""
echo "Installing hub..."
cd /usr/local/hub
sudo ./script/build
wait

echo ""
echo "Moving hub binary to a location that is in \$PATH"
sudo cp /usr/local/hub/bin/hub /usr/sbin/hub
wait

echo ""
echo "Aliasing hub as git..."
echo eval \"\$\(hub alias -s\)\" >> ~/.bashrc
wait

echo ""
echo "Setting up git config"
git config --global user.email rpidaseditor@gmail.com
git config --global user.name RPiDASTeam

echo "Use \"git config\" for help on resetting these values, or edit the file ~/.gitconfig"

# Set to Seattle Config
echo ""
echo "Setting config to Seattle RPi DAS defaults"
source /kwh/config.conf; seattle

# Activate cron jobs
echo ""
echo "Enabling cron jobs for reading sms, transmitting data, and updating the time"
wait
sudo cp /kwh/moves/dcrond /etc/cron.d/dcrond
wait
sudo chmod 644 /etc/cron.d/dcrond
wait

# Reboot to finalize
echo ""
echo "Installation complete. A reboot is necessary to enable communications with the"
echo "PCB or other hardware solution."
echo ""
echo "If you would like kwh to host your data, please contact us."
echo "You can contact us and/or donate to KiloWatts for Humanity at" 
echo "http://KiloWattsforHumanity.org"
echo ""
echo "Rebooting now is highly recommended, as some communications will be erroring"
echo "and filling log files. However, if you need to stop the reboot, you can use"
echo "\"ctrl+c\" to kill this process without rebooting"
echo "Press enter to reboot now..."
read ans
sudo shutdown -r now
fi
