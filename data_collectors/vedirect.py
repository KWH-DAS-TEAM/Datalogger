#!/usr/bin/python
# -*- coding: utf-8 -*-
# Built and tested with Python 2.7.13

# =================================================
# Charge Controller Processing
# 2020 Capstone Team CS 20.10
# Audrey Kan, Ben Targan, Dalena Le, Jesse DuFresne
# =================================================

import sys
import os, serial, argparse
import serial.tools.list_ports as listPorts
import subprocess
import time
sys.path.append('/kwh/lib')
import KWH_MySQL

# Load environment variables for KWH debug flag
exec(open("/kwh/config/get_config.py").read())
DEBUG = int(config_var['DEBUG'])

# KWH Log function
def log(logText):
    with open("/kwh/log/modbus.log", "a+") as log:
        log.write(str(int(time.time())) + ": " + logText +"\n")




##############################################################################
class vedirect:
    
    def __init__(self, serialport, timestamp):
        self.timestamp = timestamp
        self.serialport = serialport
        self.ser = serial.Serial(serialport, 19200)
        self.carrigeReturn = '\r'
        self.newLine = '\n'
        self.colon = ':'
        self.tab = '\t'
        self.key = ''
        self.value = ''
        self.packetLen = 0
        self.currState = self.WAIT_HEADER
        self.packetDict = {}


    # constants
    (HEX, WAIT_HEADER, IN_KEY, IN_VALUE, IN_CHECKSUM) = range(5)

#-----------------------------------------------------------------------------
    # input loop, one byte at a time
    def input(self, byte):
        if byte == self.colon and self.currState != self.IN_CHECKSUM:
            self.currState = self.HEX
            
        #---------------------------------------------------------------------
        
        if self.currState == self.WAIT_HEADER:

            try:
                self.packetLen += ord(byte) #ord throws: given char arr len 0

            except TypeError:
                pass
            if byte == self.carrigeReturn:
                self.currState = self.WAIT_HEADER
            
            elif byte == self.newLine:
                self.currState = self.IN_KEY

            return None

        #---------------------------------------------------------------------

        elif self.currState == self.IN_KEY:
            try:
                self.packetLen += ord(byte)

            except TypeError:
                pass
            if byte == self.tab:
                if (self.key == 'Checksum'):
                    self.currState = self.IN_CHECKSUM
                
                else:
                    self.currState = self.IN_VALUE
            
            else:
                self.key += byte
            
            return None
        
        #---------------------------------------------------------------------        

        elif self.currState == self.IN_VALUE:
            try:
                self.packetLen += ord(byte)

            except TypeError:
                pass
            if byte == self.carrigeReturn:
                self.currState = self.WAIT_HEADER
                
                self.packetDict[self.key] = self.value
                self.key = ''
                self.value = ''
            
            else:
                self.value += byte
            
            return None

        #---------------------------------------------------------------------

        elif self.currState == self.IN_CHECKSUM:
            try:
                self.packetLen += ord(byte)
            except TypeError:
                pass
            self.key = ''
            self.value = ''
            self.currState = self.WAIT_HEADER
            
            if (self.packetLen % 256 == 0):
                self.packetLen = 0
                return self.packetDict #VALID PACKET RETURN

            else:
                self.packetLen = 0

        #---------------------------------------------------------------------                

        elif self.currState == self.HEX:
            self.packetLen = 0

            if byte == self.newLine:
                self.currState = self.WAIT_HEADER

        #---------------------------------------------------------------------

        else:
            raise AssertionError()
            

#-----------------------------------------------------------------------------

    def read(self, sendingFunction):
        foundCompletePacket = False
        # sends one packet per execution
        while not foundCompletePacket:
            byte = self.ser.read(1)
            if byte:
                try:
                    packet = self.input(byte.decode('windows-1252', errors="ignore"))
                except UnicodeError:
                    packet = self.input(byte.decode('utf-8', errors="ignore"))

                if (packet != None):
                    foundCompletePacket = True
                    sendingFunction(packet, self.timestamp)
            else:
                log("No byte read over serial, break occured.")
                break
##############################################################################

def convertKeys(data):
    # unnecessary substitutions commented out, left here to show complete packet keys
    keysDict = {
        "PPV" : "PVArrayPower",
        "VPV" : "PVArrayVoltage",
        # "LOAD" : "Load",
        # "H19" : "h19",
        # "Relay" : "Relay",
        "ERR" : "Error",
        # "FW" : "FW",
        "I" : "MainCurrent",
        # "H21" : "h21",
        # "PID" : "PID",
        # "H20" : "h20",
        # "H23" : "h23",
        "MPPT" : "MaximumPowerPoint",
        # "HSDS" : "HSDS",
        "SER#" : "Serial",
        "V" : "MainVoltage"#,
        # "CS" : "CS",
        # "H22" : "h22",
        # "OR" : "OR"
    }
    newdata = {}

    for key in data:

        try:
            newdata[keysDict[key]] = data[key]
        except KeyError:
            newdata[key] = data[key]

    return newdata

#-----------------------------------------------------------------------------

def convertNonNumeric(value):
    if value == "ON":
        return 1

    elif value == "OFF":
        return 0

    #TODO: other non numeric results?

    #if none of these cases, already numeric
    return value

#-----------------------------------------------------------------------------

def sendToSQL(data, timestamp):
    data = convertKeys(data)
    DB = KWH_MySQL.KWH_MySQL()

    # keys added here will be excluded from insertion into SQL
    excludedKeys = [
        "Serial"#cannot be converted to numeric
    ]

    for key in data:
        if key in excludedKeys:
            continue

        # if value is hex, convert it to decimal
        if data[key][:2] == "0x":
            i  = int(data[key], 16)
            sql="INSERT INTO data VALUES (" + str(timestamp) +",\""+ str(key) + "\"," + str(i) + ");"

        else:
            value = convertNonNumeric(data[key])

            sql="INSERT INTO data VALUES (" + str(timestamp) +",\""+ str(key) + "\"," + str(value) + ");"
        

        DB.INSERT(sql)
        if DEBUG: log(sql)

#-----------------------------------------------------------------------------
# for debugging
def printToConsole(data, timestamp):

    data = convertKeys(data)

    print("-----------------------------------------------------")
    for key in data:
        # if value is hex, convert it to decimal
        if data[key][:2] == "0x":
            i  = int(data[key], 16)
            print("(%s)%s : %s" % (timestamp, key.encode("utf-8"), str(i)))
        else:
            value = convertNonNumeric(data[key])    
            print("(%s)%s : %s" % (timestamp, key.encode("utf-8"), str(value)))
    print("-----------------------------------------------------")

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    timestamp = sys.argv[1]
    correctPort = ''
    
    while correctPort == '':
        
        possiblePorts = listPorts.comports()

        for port in possiblePorts:
            if port.description == 'VE Direct cable':
                correctPort = port.device


        if correctPort == '':
            log("Serial Port for Charge Controller not found, retrying...")


    ve = vedirect(correctPort, timestamp)

    # swap sendToSQL with printToConsole for debugging
    ve.read(sendToSQL) 

    log("Packet sent, exiting...")