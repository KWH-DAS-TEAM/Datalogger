#!/usr/bin/env python3
import KWH_MySQL
import sys
sys.path.append('/kwh/lib')

try:
    key = sys.argv[1]
except:
    print("Usage: delconf <key> (optional: 1 deletes history)")
    exit(1)

kill_history = False

if len(sys.argv) > 2:
    value = sys.argv[2]
    if value == "1":
        kill_history = True

DB = KWH_MySQL.KWH_MySQL()

if kill_history:
    sql = "DELETE FROM config WHERE `key` = \"" + key + "\";"
else:
    select_sql = "SELECT max(active) FROM config WHERE `key` = '"+key+"';"
    new_active = DB.SELECT(select_sql)[0][0] + 1

    sql = "UPDATE config SET time_changed = now(), active = "
    sql += str(new_active)+" WHERE `key` = '"+key+"' AND active = 1;"

# Returns 1 on failure
result = DB.INSERT(sql)
if result[0] == 1:
    print(result[1])
exit(result[0])
