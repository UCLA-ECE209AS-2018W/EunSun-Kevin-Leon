#!/bin/csh

python2 rm_rule.py /conf/config.xml $1 $2
mv new_config.xml /conf/config.xml
rm -rf /tmp/config.cache
/etc/rc.filter_configure
