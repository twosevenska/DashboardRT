#!/usr/bin/env python
from pprint import pprint

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api import RTApi
#from ditic_kanban.statistics import stats_read_json_file
#from ditic_kanban.statistics import get_statistics
#from ditic_kanban.statistics import full_list_of_tickets_on_a_date
from ditic_kanban.rt_projects import get_project_tree
from ditic_kanban.rt_projects import ManageProjectElements

config = DITICConfig()
system = config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])

#for aux in range(0, 30):
#    print get_date(aux),
#    print stats_number_of_tickets_of_an_user(rt_object, 'flaviopereira@uc.pt', get_date(aux))
#print stats_update_json_file(28)
#result = stats_read_json_file('2015', '07')
#for day in sorted(result):
#    print day,
#    print 'Created:', result[day]['created_tickets'],
#    print 'Resolved:', result[day]['team']['resolved'],
#    print 'Open:', result[day]['team']['open']
#    print 'Mean time: %0.2f' % result[day]['team']['mean_time_to_resolve']
#pprint(get_statistics('2015-05-01', '2015-07-30'))
#result = full_list_of_tickets_on_a_date(rt_object, config, '2015-07-25')
#pprint(result)

# Project examples:
# 885775
#	887677
#	897183
#   899145
#       899148

project_management = ManageProjectElements()
pprint(get_project_tree(rt_object, project_management, 885775))



