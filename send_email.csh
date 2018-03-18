#!/bin/csh

SRC_IP=$1
DST_IP=$2

echo External IP address $SRC_IP is trying to talk to $DST_IP. Should $SRC_IP be added to the whitelist? | /usr/local/bin/mail.php -s"Subject: New ip address detected!"
