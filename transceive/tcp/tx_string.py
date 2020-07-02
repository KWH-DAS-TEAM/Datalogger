#!/usr/bin/env python3
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')

# load kwh environment variables from config
exec(open("/kwh/config/get_config.py").read())
timestamp = sys.argv[1]

# build database object
DB = KWH_MySQL.KWH_MySQL()

# setup the transmission string (tx_string)
tx_string = config_var['ADMPW']+"#STA:" + config_var['STA'] + ";TM:"+timestamp
data = DB.SELECT(
    "SELECT `key`, value FROM data WHERE timestamp = "+timestamp+";")

for pair in data:
    tx_string += ";" + str(pair[0]) + ":" + str(pair[1]).rstrip("0")

# Finish string
tx_string += "#"

# Write to tx_string table
sql = "INSERT INTO tx_string VALUES (" + timestamp + ",\"" + tx_string + "\");"
DB.INSERT(sql)
