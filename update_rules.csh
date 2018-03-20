#!/bin/csh

easyrule pass $1 any $2 $3
python2 xml_parser.py /conf/config.xml $1 $2 $3
mv new_config.xml /conf/config.xml
rm -rf /tmp/config.cache
/etc/rc.filter_configure
