#!/usr/bin/python2.7

import subprocess

import re
import json
import datetime

def timetostr(time):
    return time.strftime('%Y-%m-%d:%H:%M:%S')

def strtotime(key):
    return datetime.strptime(key,'%Y-%m-%d:%H:%M:%S' )

def timedifference(a,b):
    return ((a-b).seconds)


def add_whitelist(sourceip, destinationip):
    dict_list = []
    print(sourceip, destinationip)
    #open dictionary text file
    with open(white_f, 'r') as file:
        json_dict = file.read()
        if (json_dict): whitelist_dict = json.loads(json_dict)
        else: 
            whitelist_dict = {}
        #checks if the sourceip address exists
        if sourceip in whitelist_dict:
            #sourceip address exists
            #checks if the destinationip address exists
            if destinationip not in whitelist_dict[sourceip]:
                whitelist_dict[sourceip].append(destinationip)
            #print(whitelist_dict[sourceip])
        else:
            print("the key does not exist")
#             print(sourceip, destinationip)
            current_time =  timetostr(datetime.datetime.now())
            dict_list = [current_time, destinationip]
            whitelist_dict.update({sourceip:dict_list})
            
    with open(white_f, 'w') as file:
        file.write(json.dumps(whitelist_dict)) # use `json.loads` to do the reverse
	
	subprocess.call(["./update_rules.csh", sourceip, destination_ip])


        
def filterlog_search(filename, searchtext1, searchtext2):
    h = 0 
    returntypes  = ['date/time','rulenumber','interface','source_ip','source_port','destination_ip','destination_port','protocol']
    with open(filename) as f:
        for line in f:
            if searchtext1 in line:
                if searchtext2 in line:
                    logline_list = [x.strip() for x in line.split(',')]
                    if(len(logline_list) == 23):
                        if(logline_list[0][16:34] == 'pfSense filterlog:'):
                            date_time = logline_list[0] #date/time
                            rulenumber = logline_list[3] #rulenumber
                            interface = logline_list[4] #interface
                            pass_block = logline_list[6] #pass/block
                            source_ip = logline_list[18] #source_ip
                            destination_ip = logline_list[19] #destination_ip
                            protocol = logline_list[16] #protocol
#                             print(source_ip)
#                             if returntype == 0: output = logline_list[0] #date/time
#                             if returntype == 1: output = logline_list[3] #rulenumber
#                             if returntype == 2: output = logline_list[4] #interface
#                             if returntype == 3: output = logline_list[6] #pass/block
#                             if returntype == 4: output = logline_list[18] #source_ip
#                             if returntype == 5: output = logline_list[19] #destination_ip
#                             if returntype == 6: output = logline_list[16] #protocol
                            add_whitelist(source_ip,destination_ip)
#                             print(source_ip,destination_ip)


log_f = 'testlogfile.log'
white_f = 'whitelist.txt'

searchtext1 = 'block'
searchtext2 = 'ue0'
#returntypes  = ['0:date/time','1:rulenumber','2:interface','3:pass/block','4:source_ip','5:destination_ip','6:protocol'
#'7:source_port','8:destination_port']
filterlog_search(log_f, searchtext1, searchtext2)

