#!/usr/bin/env python3
import signal
import minimalmodbus
import time
import sys
sys.path.append('/kwh/lib')
import KWH_MySQL

# Load environment variables
exec(open("/kwh/config/get_config.py").read())
DEBUG = int(config_var['DEBUG'])
timestamp=sys.argv[1]

def signal_handler(signal, frame):
    if DEBUG > 0: log('SIGINT received...killing modbus gracefully')
    exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Log function
def log(logText):
    with open("/kwh/log/modbus.log", "a+") as log:
        log.write(str(int(time.time())) + ": " + logText +"\n")

minimalmodbus.PARITY='E'
minimalmodbus.BAUDRATE=9600
minimalmodbus.STOPBITS=1
minimalmodbus.BYTESIZE=8
minimalmodbus.TIMEOUT=1
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True

DB = KWH_MySQL.KWH_MySQL()

for i in range(2,int(config_var['MAX_MODBUS_COUNT'])+2):
    try:
        mb=minimalmodbus.Instrument('/dev/ttyUSB0', i, mode='rtu')
        if config_var['MB_VOLTAGE'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="Voltage\","+str(mb.read_float(0, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_CURRENT'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="Current\","+str(mb.read_float(6, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_ACTIVE_POWER'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ActivePower\","+str(mb.read_float(12, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_APPARENT_POWER'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ApparentPower\","+str(mb.read_float(18, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_REACTIVE_POWER'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ReactivePower\","+str(mb.read_float(24, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_POWER_FACTOR'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="PowerFactor\","+str(mb.read_float(30, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_PHASE_ANGLE'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="PhaseAngle\","+str(mb.read_float(36, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_FREQUENCY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="Frequency\","+str(mb.read_float(70, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_IMPORT_ACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ImportActiveEnergy\","+str(mb.read_float(72, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_EXPORT_ACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ExportActiveEnergy\","+str(mb.read_float(74, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_IMPORT_REACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ImportReactiveEnergy\","+str(mb.read_float(76, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_EXPORT_REACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="ExportReactiveEnergy\","+str(mb.read_float(78, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_TOTAL_ACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="TotalActiveEnergy\","+str(mb.read_float(342, 4, 2))+");"
            DB.INSERT(sql)

        if config_var['MB_TOTAL_REACTIVE_ENERGY'] == "1":
            sql="INSERT INTO data VALUES ("+timestamp+",\"M"+str(i)
            sql+="TotalReactiveEnergy\","+str(mb.read_float(344, 4, 2))+");"
            DB.INSERT(sql)

    except:
        log("No response from address "+str(i))
