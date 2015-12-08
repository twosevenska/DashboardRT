#!/usr/bin/env python

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api_old import get_list_of_tickets
from ditic_kanban.rt_api_old import RTApi

myconfig = DITICConfig()
system = myconfig.get_system()

email_rt_api = RTApi(system['server'], system['username'], system['password'])

#query = 'Owner = "vapi@uc.pt" and Status = "rejected"'
query = '"cf.{is - informatica e sistemas}" like "dir" and "cf.{is - informatica e sistemas}" not like "dir-inbox"'

response = myconfig.check_if_user_exist(system['username'])
print "%s\n" % str(response)

response = get_list_of_user(email_rt_api, query)
for k in response:
    print k

print len(response)
