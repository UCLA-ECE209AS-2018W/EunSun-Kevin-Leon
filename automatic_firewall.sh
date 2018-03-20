#!/bin/sh
echo started
sleep 10
while [ 1 ]
do 
  python2 /root/update_whitelist.py
  python2 /root/verify_whitelist.py
  sleep 10
done
