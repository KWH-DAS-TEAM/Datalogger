#!/usr/bin/env python3
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')
#import Bit_Bang_ADC

# load kwh environment variables from config
exec(open("/kwh/config/load_config.py").read())
timestamp = sys.argv[0]
config = [config_var['PU01'],
          config_var['PU02'],
          config_var['PU03'],
          config_var['PU04'],
          config_var['PU05'],
          config_var['PU06']]
#          config_var['PU07'],
#          config_var['PU08']]

for i in range(6):
    if config[i] == '1':
        j = i+1  # add one to get to PU01 instead of PU00
        # grab the value from the PU01-6 file
        value = open("/kwh/data_collectors/pulse/PU0" + str(j), 'r').read()
        # write into the data table
        sql_insert = "INSERT INTO `data` VALUES (now(), 'PU0" + \
            str(j)+"', "+value+")"
        result = DB.INSERT(sql_insert)
