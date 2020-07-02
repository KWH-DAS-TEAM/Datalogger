#!/usr/bin/env python3
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')

try:
    APN = sys.argv[1]
except:
    print("Usage: setapn <APN> <optional Username> <optional Password>")
    exit(1)

try:
    USER = sys.argv[2]
except:
    USER = " "
try:
    PASS = sys.argv[3]
except:
    PASS = " "

DB = KWH_MySQL.KWH_MySQL()

sql = "INSERT INTO config VALUES (\"APN\",\""+APN+"\",now(),\"\",1);"

# Returns 1 on failure
result = DB.INSERT(sql)[0]

# INSERT will fail for duplicate entry if the config key already exists
# due to our primary key (key, active). This lets us force only one key
# having active = 1
# If insert fails, the following logic keeps a historical record of the
# previous config, and then lets you update with the new value
if result == 1:
    select_sql = "SELECT max(active) FROM config WHERE `key` = 'APN';"
    new_active = DB.SELECT(select_sql)[0][0] + 1

    update_sql = "UPDATE config SET time_changed = now(), active = "
    update_sql += str(new_active)+" WHERE `key` = 'APN' AND active = 1;"
    result = DB.INSERT(update_sql)
    if result == 1:
        print("unknown error")
    else:
        DB.INSERT(sql)

sakis = open("/etc/sakis3g.conf", "w+")
sakis.write("OTHER=CUSTOM_TTY\nCUSTOM_TTY=\"/dev/ttyAMA0\"\nBAUD=115200\nAPN=\"" +
            APN+"\"\nAPN_USER=\""+USER+"\"\nAPN_PASS=\""+PASS+"\"")

print("config change complete")
