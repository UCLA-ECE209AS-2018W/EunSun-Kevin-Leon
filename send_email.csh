#!/bin/csh
echo "External IP address $1 is trying to talk to $2. Should $1 be added to the whitelist?" | /usr/local/bin/mail.php -s"Subject: New ip address detected!"
