#!/bin/sh
echo started
sleep 10
while [ 1 ]
do
  echo Blah 
  python2 /root/update_whitelist.py
  sleep 30
done
