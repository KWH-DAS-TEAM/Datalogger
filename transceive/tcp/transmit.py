#!/usr/bin/env python3
import zlib
import KWH_MySQL
import socket
import sys
sys.path.append('/kwh/lib')

# load config variables from kwh.config table
exec(open("/kwh/config/get_config.py").read())
DEBUG = int(config_var['DEBUG'])

# Grab up to 100 tx_strings and tx them
DB = KWH_MySQL.KWH_MySQL()
records = DB.SELECT("SELECT * FROM tx_string LIMIT 100;")

for row in records:
    if config_var['COMPRESS'] == "1":
        bytedata = bytearray()
        bytedata = zlib.compress(row[1], 6)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if DEBUG:
        print(config_var['DOMAIN'])
    if DEBUG:
        print(config_var['PORT'])
    server.connect((config_var['DOMAIN'], int(config_var['PORT'])))
    server.send(bytedata)
    rcv = server.recv(1024)
    server.close()
    if int(rcv) == row[0]:
        DB = KWH_MySQL.KWH_MySQL()
        sql = "DELETE FROM kwh.tx_string WHERE timestamp = " + str(row[0])
        result = DB.INSERT(sql)
