__author__ = 'edd'

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api_old import RTApi

config = DITICConfig()
system = config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])