#!/usr/bin/python2.7
import sys
import fileinput
import string

inputfile = open(sys.argv[1], 'r')
outputfile = open("new_config.xml", 'w')

lines = inputfile.readlines()

found = False
i = 0
for line in lines:
    if "<username>Leon Test"+sys.argv[2]+sys.argv[3]+"</username>" in line:
        found = True
        break
    i += 1

# new_rule = lines[(i-13):(i+3)]
if found:
    del lines[(i-13):(i+3)]
'''
if sys.argv[2] == "lan":
    i = 0
    for line in lines:
        if "<descr><![CDATA[Block all traffic going to WAN]]></descr>" in line:
            break
        i += 1

    j = 0
    for line in new_rule:
        lines.insert((i-23 + j), line)
        j += 1
else:
    i = 0
    for line in lines:
        if "<descr><![CDATA[Block all incoming traffic Leon]]></descr>" in line:
            break
        i += 1

    j = 0
    for line in new_rule:
        lines.insert((i-22 + j), line)
        j += 1
'''
outputfile.writelines(lines)
# close the file after reading the lines.
inputfile.close()
outputfile.close()
'''
f = fileinput.FileInput("new_config.xml", inplace=True, backup='.bak')
for line in f:
    sys.stdout.write(string.replace(line, "<username>Easy Rule</username>", "<username>Leon Test</username>"))
f.close()
'''
