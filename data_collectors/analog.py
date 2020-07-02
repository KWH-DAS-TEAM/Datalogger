#!/usr/bin/env python3
import Bit_Bang_ADC
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')

# load kwh environment variables from config
exec(open("/kwh/config/get_config.py").read())
timestamp = sys.argv[1]

################################################################################
# 1. The RPi GPIO pins for the ADC are hard coded into Bit_Bang_ADC.py
################################################################################
# 2. The ADC has 12 bits and upon request from the RPi it responds with numbers
# from 0 to 4095. If the sensed voltage = the comparison voltage, the ADC will
# respond with 4095. If the sensed voltage is half the comparison voltage, the
# ADC will respond with 2048.
# i.e. ADC reported voltage = (x/4096) * comparison voltage, where x is the
# number the ADC responds with.
################################################################################
# 3. Not every request the pi sends to the ADC gets an accurate response. With a
# large enough set of respones, the majority are accurate. This logic takes a
# set of samples and orders them from smallest to largest. Placing the set in
# numerical order puts the low and high outliers at the beggining and end of the
# array. The logic then looks at the middle of the array and computes a mean
# average.
# e.g. Logic asks for 7 samples and the chip responds with:
#      1002, 45, 1007, 4003, 4095, 1008, 2
# These are ordered to: 2, 45, 1002, 1007, 1008, 4003, 4095
# Then logic takes a mean average of the center three: (1002 + 1007 + 1008) / 3
# 1005.666 is then divided by 4095 to see the ratio of the comparison voltage.
# The logic then uses the equation from (2.) to report the voltage...~1.25 V
################################################################################

samples = 21
cmpr_voltage = 5.0  # update to 5.0 with Rev.2 PCB thanks to Voltage reference chip
skewing_percentage = 1.0
bias = 0.000

# instantiating needed arrays
value = []
channel = []
config = [config_var['AD01'],
          config_var['AD02'],
          config_var['AD03'],
          config_var['AD04'],
          config_var['AD05'],
          config_var['AD06'],
          config_var['AD07'],
          config_var['AD08']]

# collecting samples in channel array where each element is a value array for that channel
for j in range(8):
    if config[j] == '1':
        for i in range(samples):
                # using this because unable to append 1st element
            if i == 0:
                value = [Bit_Bang_ADC.readadc(j)]
            else:
                value.append(Bit_Bang_ADC.readadc(j))
        # using this because unable to append 1st element
        if j == 0:
            channel = [sorted(value)]
        else:
            channel.append(sorted(value))

# computing responses and storing in values[]
# grabbing the middle third of the data to ignore outliers
values = [0]*8
for i in range(8):
    if config[i] == '1':
        values[i] = (channel[i][int(len(channel[i])/2-2)] +
                     channel[i][int(len(channel[i])/2-1)] +
                     channel[i][int(len(channel[i])/2)] +
                     channel[i][int(len(channel[i])/2+1)] +
                     channel[i][int(len(channel[i])/2+2)]) / 5
    else:
        values[i] = 0.0

# compute the values and insert into data table
DB = KWH_MySQL.KWH_MySQL()

for i in range(8):
    if config[i] == '1':
        values[i] = (values[i]/4095.0) * cmpr_voltage * \
            skewing_percentage - bias
        sql_insert = "INSERT INTO `data` VALUES ("+timestamp + \
            ", 'A"+str(i+1)+"', "+str(values[i])+");"
        result = DB.INSERT(sql_insert)
