#!/usr/bin/env python3
import sys
import zlib

# load config variables from kwh.config table
exec(open("/kwh/config/get_config.py").read())

data = sys.argv[1]
bytedata = bytearray()
bytedata = zlib.compress(bytes(data, 'utf-8'), 6)
sys.stdout.buffer.write(bytedata)
