#!/bin/csh

easyrule pass lan any $1 $2
python2 xml_parser.py /conf/config.xml
mv new_config.xml /conf/config.xml
rm -rf /tmp/config.cache
/etc/rc.filter_configure