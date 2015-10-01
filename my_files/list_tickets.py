#!/usr/bin/env python

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api import get_list_of_tickets
from ditic_kanban.rt_api import RTApi

myconfig = DITICConfig()
system = myconfig.get_system()

email_rt_api = RTApi(system['server'], system['username'], system['password'])

#query = 'Owner = "vapi@uc.pt" and Status = "rejected"'
query = '"cf.{is - informatica e sistemas}" not like "dir" and "cf.{is - informatica e sistemas}" not like "dir-inbox"'

response = get_list_of_tickets(email_rt_api, query)

print response
print len(response)
