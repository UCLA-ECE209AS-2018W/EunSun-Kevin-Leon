#!/bin/csh
echo "IP address $1 was found on blacklist so we removed the rule that communicates with IP address $2." | /usr/local/bin/mail.php -s"IP found on blacklist- rule removed!"
