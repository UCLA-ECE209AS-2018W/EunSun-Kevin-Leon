
import subprocess

import re
import json
import datetime

def mailnotification(sourceip, destinationip):

    subprocess.call(["./send_email_rm.csh", sourceip, destinationip])

def remove_rules(sourceip,destinationip):
    
    subprocess.call(["./rm_rule.csh", sourceip, destinationip])

def verify_whitelist():
    white_f = 'whitelist.txt'

    blacklist = []
    with open('blacklist.txt','r') as f:
        for black_ip in f:
            blacklist.append(black_ip.split()[0])


    whitelist_dict = {}
    with open(white_f, 'r') as file:
            json_dict = file.read()
            if (json_dict): 
                whitelist_dict = json.loads(json_dict)
                # print("original:")
                # print(whitelist_dict)

                deletelist = []

                for i in whitelist_dict:
#                     print(i)
                    if i in blacklist:
                        deletelist.append(i)
                        for k in whitelist_dict[i]:
                            remove_rules(i,k)
                            print "Rule successfully removed_found from source ip list"
                            mailnotification(i,k)

                for t in deletelist:
                    del whitelist_dict[t]

                for i in whitelist_dict:
                    for k in blacklist:
                        for t in whitelist_dict[i]:
                            if t == k: 
#                                 sourceip = i
#                                 destinationip = t
                                whitelist_dict[i].remove(t)
                                remove_rules(i,t)
                                print "Rule successfully removed_found from destination ip list"
                                mailnotification(t, i)

#     print("updated:")


#     print(whitelist_dict)
                                #delete from whitelist
                with open(white_f, 'w') as file:
                    file.write(json.dumps(whitelist_dict))


verify_whitelist()


