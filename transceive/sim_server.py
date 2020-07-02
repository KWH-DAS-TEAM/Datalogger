#!/usr/bin/env python3
import KWH_MySQL
import socket
import time
import signal
import serial
import subprocess
import sys
sys.path.append('/kwh/lib')

# Load environment variables
exec(open("/kwh/config/get_config.py").read())
DEBUG = int(config_var['DEBUG'])

# Global variables
RESET_LIMIT = 3


def signal_handler(signal, frame):
    if DEBUG > 0:
        log('SIGINT received...Closing SIM Server\n')
    sim.close()
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    cs.shutdown(socket.SHUT_RDWR)
    cs.close()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Log function


def log(logText):
    with open("/kwh/log/sim_server.log", "a") as log:
        log.write(str(int(time.time())) + ": " + logText)

# Reset the SIM card


def reset():
    exec(open("/kwh/transceive/reset_sim.py").read())
    if DEBUG > 0:
        log("Sleeping 5 for SIM reboot and reconfigure!\n")
    time.sleep(4)


# Logs in simServer.log if the env variable DEBUG is 1
if DEBUG > 0:
    log("Starting SIM Server\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 9999
port_chosen = False

if DEBUG > 0:
    log("Starting port selection\n")

# Find an open port for the service
while not port_chosen:
    try:
        s.bind((host, port))
        port_chosen = True
    except:
        if DEBUG > 0:
            log("Port "+str(port)+" in use\n")
        port = port + 1

# Update the env variables with the chosen active SIM_PORT
DB = KWH_MySQL.KWH_MySQL()
subprocess.call(["/kwh/config/set_config.py", "SIM_PORT", str(port)])
if DEBUG > 0:
    log("SIM_PORT: "+str(port)+"\n")

# Configure block
reset()
subprocess.Popen("/kwh/transceive/ttyAMA0_setup.sh")
if DEBUG > 1:
    log("Executed ttyAMA0_setup.sh\n")
time.sleep(1)

s.listen(1)
sim = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)
sim.flushInput()
sim.flushOutput()
if DEBUG > 0:
    log("Listening...\n")

# Daemon listen on SIM_PORT for SIM commands
while True:
    # Waits for a command
    cs, addr = s.accept()

    # Configure block
    exec(open("/kwh/config/get_config.py").read())
    DEBUG = int(config_var['DEBUG'])
    if DEBUG > 1:
        log("Configuration variables reloaded\n")
    subprocess.Popen("/kwh/transceive/ttyAMA0_setup.sh")
    if DEBUG > 1:
        log("Executed ttyAMA0_setup.sh\n")

    # Beginning to process received command
    cmd = cs.recv(300000)
    try:
        if DEBUG > 1:
            log("Received: "+cmd.decode('UTF-8')+"\n")
    except:
        pass
    # Send command to SIM
    try:
        sim.write(cmd)

        if DEBUG > 0:
            log("Wrote to sim: "+cmd.decode('UTF-8')+"\n")

        # Command specific delays
        if cmd.decode('UTF-8') == "AT+CGATT=1\n" \
                or cmd.decode('UTF-8') == "AT+CIFSR\n" \
                or cmd.decode('UTF-8')[0] == "\#":
            time.sleep(3)
        elif cmd.decode('UTF-8') == "AT+CIPSTART=\"TCP\",\""+config_var['DOMAIN']+"\",\""+config_var['PORT']+"\"\n" \
                or cmd.decode('UTF-8') == "AT+CIICR\n" \
                or cmd.decode('UTF-8') == "AT+CIPSTART=\"TCP\",\"time.nist.gov\",\"37\"\n":
            time.sleep(4)
        else:
            time.sleep(.3)

        # Get SIM response
        fromSIM = sim.inWaiting()

        # If no response, restart SIM, reset config, and retry
        count = 0
        while fromSIM < 1 and count < RESET_LIMIT:
            # Check one more time before resetting
            time.sleep(1)
            fromSIM = sim.inWaiting()
            if fromSIM > 0:
                break
            if DEBUG > 0:
                log(str(fromSIM)+" bytes from SIM. Resetting SIM!\n")
            # No luck! Reset
            reset()
            exec(open("/kwh/config/get_config.py").read())
            DEBUG = int(config_var['DEBUG'])
            if DEBUG > 1:
                log("Configuration variables reloaded\n")
            subprocess.Popen("/kwh/transceive/ttyAMA0_setup.sh")
            if DEBUG > 1:
                log("Executed ttyAMA0_setup.sh\n")
            time.sleep(1)

            count += 1
            # Resend command and check again for response
            try:
                sim.write(cmd)
            except:
                log("EXCEPTION: Write Failed\n")
            if DEBUG > 0:
                log("Wrote to sim: "+cmd.decode('UTF-8')+"\n")
            time.sleep(0.5)
            fromSIM = sim.inWaiting()

        # Get SIM response
        if DEBUG > 0:
            log("Bytes to read: "+str(fromSIM)+"\n")
        resp = sim.read(fromSIM)
        if DEBUG > 0:
            log("Sim response: "+resp.decode('UTF-8')+"\n")
        # Tell the client if there was "No response" failure
        if resp.decode('UTF-8') == "":
            resp = bytes("No response", 'UTF-8')
        cs.send(resp)
        if DEBUG > 1:
            log("Response sent to: "+str(addr)+"\n")

        # Check for any other response data in SIM memory
        fromSIM = sim.inWaiting()
        if fromSIM > 0:
            if DEBUG > 0:
                log("Bytes to read: "+str(fromSIM)+"\n")
            resp = sim.read(fromSIM)
            if DEBUG > 0:
                log("Sim response: "+resp.decode('UTF-8')+"\n")
            cs.send(resp)
            if DEBUG > 1:
                log("Response sent to: "+str(addr)+"\n")

        sim.flushInput()
        sim.flushOutput()

        time.sleep(.5)
        cs.shutdown(socket.SHUT_RDWR)
        cs.close()
    except:
        log("EXCEPTION: Write Failed\n")
        reset()
        exec(open("/kwh/config/get_config.py").read())
        DEBUG = int(config_var['DEBUG'])
        if DEBUG > 1:
            log("Configuration variables reloaded\n")
        subprocess.Popen("/kwh/transceive/ttyAMA0_setup.sh")
        if DEBUG > 1:
            log("Executed ttyAMA0_setup.sh\n")
        time.sleep(1)

    if DEBUG > 1:
        log("Client connection closed\n")
