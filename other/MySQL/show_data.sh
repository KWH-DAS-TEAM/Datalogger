#!/bin/bash
echo 'SELECT timestamp FROM kwh.data WHERE `key` like "'$1%\" LIMIT 1 | mysql -u pi
echo 'SELECT `key`, `value` FROM kwh.data WHERE `key` like "'$1%\" | mysql -u pi
