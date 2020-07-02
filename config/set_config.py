#!/usr/bin/env python3
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')

try:
    key = sys.argv[1]
    value = sys.argv[2]
except:
    print("Usage: setconf <key> <value>")
    exit(1)

DB = KWH_MySQL.KWH_MySQL()

sql = "INSERT INTO config VALUES (\""+key+"\",\""+value+"\",now(),\"\",1);"

# Returns 1 on failure
result = DB.INSERT(sql)[0]

# INSERT will fail for duplicate entry if the config key already exists
# due to our primary key (key, active). This lets us force only one key
# having active = 1
# If insert fails, the following logic keeps a historical record of the
# previous config, and then lets you update with the new value
if result == 1:
    select_sql = "SELECT max(active) FROM config WHERE `key` = '"+key+"';"
    new_active = DB.SELECT(select_sql)[0][0] + 1

    update_sql = "UPDATE config SET time_changed = now(), active = "
    update_sql += str(new_active)+" WHERE `key` = '"+key+"' AND active = 1;"
    result = DB.INSERT(update_sql)
    if result == 1:
        print("unknown error")
    else:
        DB.INSERT(sql)

print("config change complete")
