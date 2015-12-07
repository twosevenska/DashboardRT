#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Logic Box @2015
# This module is responsible for web routing. This is the main web server.

import actions
import detail
from time import time
from datetime import date


from bottle import get
from bottle import post
from bottle import put
from bottle import template
from bottle import request
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file

from new_ditic_kanban.auth import UserAuth
from new_ditic_kanban.config import DITICConfig
from new_ditic_kanban.rt_api import RTApi
from new_ditic_kanban.rt_summary import get_summary_info
from new_ditic_kanban.statistics import get_date
from new_ditic_kanban.statistics import get_statistics
from new_ditic_kanban.statistics import get_date
from new_ditic_kanban.tools import get_urgent_tickets


my_config = DITICConfig()
system = my_config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])

user_auth = UserAuth()
if user_auth.check_password(system['username'], system['password']):
	o = user_auth.get_email_id(system['username'])
else:
	print('couldnt auth')

def create_default_result():
    # Default header configuration
    result = {
        'title': 'Still testing...'
    }

    # Summary information
    result.update({'summary': get_summary_info()})

    # Mapping email do user alias
    config = DITICConfig()
    result.update({'alias': config.get_email_to_user()})

    return result

@get('/')
def get_root():
    start_time = time()

    result = create_default_result()
    # Removed to be a display at the TV
    # if request.query.o == '' or not user_auth.check_id(request.query.o):
    #    result.update({'message': ''})
    #    return template('auth', result)
    # result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'username_id': request.query.o})
    today = date.today().isoformat()
    result.update({'statistics': get_statistics(get_date(30, today), today)})

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('entrance_summary', result)


def start_server():
    run(server='paste', host='0.0.0.0', debug=True)
