#!/usr/bin/python2.7

import subprocess

import re
import json
import datetime

purge_duration = 120 #seconds = 5minutes for testing
            

def timetostr(time):
    return time.strftime('%Y-%m-%d:%H:%M:%S')

def strtotime(time):
    return datetime.datetime.strptime(time,'%Y-%m-%d:%H:%M:%S' )

def timedifference(a,b):
    return ((b-a).seconds)
    
def addrule(interface, sourceip, destinationip):
    # print ("rule added")
    subprocess.call(["./update_rules.csh", interface, sourceip, destinationip])

def mailnotification(sourceip, destinationip):
    subprocess.call(["./send_email.csh", sourceip, destinationip])

def checkmailstatus(sourceip, destinationip):
    with open(mail_f, 'r') as file:
        json_dict = file.read()
        if (json_dict): maillist_dict = json.loads(json_dict)
        else: 
            maillist_dict = {}
        if sourceip in maillist_dict:
            if destinationip not in maillist_dict[sourceip]:
                maillist_dict[sourceip].append(destinationip)
                mailnotification(sourceip, destinationip)
        else: 
            dict_list = [destinationip]
            maillist_dict.update({sourceip:dict_list})
            mailnotification(sourceip, destinationip)

    with open(mail_f, 'w') as file:
        file.write(json.dumps(maillist_dict))

def add_lan_whitelist(sourceip, destinationip):
    dict_list = []
    current_time = datetime.datetime.now()
    #open dictionary text file
    with open(white_f, 'r') as file:
        json_dict = file.read()
        if (json_dict): whitelist_dict = json.loads(json_dict)
        else: 
            whitelist_dict = {}
        if sourceip in whitelist_dict:  #checks if the sourceip address exists
            #sourceip address exists
            if destinationip not in whitelist_dict[sourceip]:  #checks if the destinationip address exists
                # time difference
                starttime = strtotime(whitelist_dict[sourceip][0])
                if timedifference(starttime,current_time) < purge_duration :
                    whitelist_dict[sourceip].append(destinationip)
                    addrule('lan' ,sourceip, destinationip)
                else:
                    checkmailstatus(sourceip,destinationip)
        else:
            dict_list = [timetostr(current_time), destinationip]
            whitelist_dict.update({sourceip:dict_list})
            addrule('lan', sourceip, destinationip) 
    with open(white_f, 'w') as file:
        file.write(json.dumps(whitelist_dict))
    

def add_wan_whitelist(sourceip, destinationip):
    dict_list = []
    current_time = datetime.datetime.now()

    #open dictionary text file
    with open(white_f, 'r') as file:
        json_dict = file.read()
        if (json_dict): whitelist_dict = json.loads(json_dict)
        else: 
            whitelist_dict = {}
        if destinationip in whitelist_dict:  # checks if the destination ip address is our iot device
            if sourceip in whitelist_dict[destinationip]: # checks if the source ip is the trusted server
                # destination ip has talked to source ip before & Add the rule
                if sourceip in whitelist_dict:  #sourceip address exists
                    if destinationip not in whitelist_dict[sourceip]:
                        whitelist_dict[sourceip].append(destinationip)
                        addrule('wan', sourceip, destinationip) 
                else:
                    dict_list = [timetostr(current_time), destinationip]
                    whitelist_dict.update({sourceip:dict_list}) 
                    addrule('wan', sourceip, destinationip)
                
    with open(white_f, 'w') as file:
        file.write(json.dumps(whitelist_dict))
    


        
def filterlog_search(filename, searchtext1):
    lansearch = 'ue0'
    wansearch = 'em0'

    
    returntypes  = ['date/time','rulenumber','interface','source_ip','source_port','destination_ip','destination_port','protocol']
    with open(filename) as f:
        for line in f:
            if searchtext1 in line: 
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

                        # checks blacklist
                        blacklist = []
                        with open('blacklist.txt','r') as f:
                            for black_ip in f:
                                blacklist.append(black_ip.split()[0])
        
                        if interface == lansearch : 
                            if destination_ip not in blacklist:
                                add_lan_whitelist(source_ip,destination_ip)
                        elif interface == wansearch : 
                            if source_ip not in blacklist:
                                add_wan_whitelist(source_ip,destination_ip)
                        

        
#log_f = 'testlog.log'
log_f = '/var/log/filter.log'
white_f = 'whitelist.txt'
mail_f = 'maillist.txt'
black_f = 'blacklist.txt'


searchtext1 = 'block'
#searchtext2 = 'ue0'
#returntypes  = ['0:date/time','1:rulenumber','2:interface','3:pass/block','4:source_ip','5:destination_ip','6:protocol'
#'7:source_port','8:destination_port']
filterlog_search(log_f, searchtext1)
