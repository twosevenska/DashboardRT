#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Logic Box @2015
# This file contains several functions that do several operations necessary to this package to work
#


from new_ditic_kanban.tools import *
from new_ditic_kanban.auth import UserAuth
from new_ditic_kanban.config import DITICConfig
from new_ditic_kanban.rt_api import RTApi


from bottle import put
from bottle import get
from bottle import post
from bottle import template
from bottle import request
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file

my_config = DITICConfig()
system = my_config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])

user_auth = UserAuth()
if user_auth.check_password(system['username'], system['password']):
	o = user_auth.get_email_id(system['username'])
else:
	print('couldnt auth') 
	
	
@put('/action/backward/<ticket_id:int>')
def on_action_backward(ticket_id):
	start_time = time()
	print("forward:"+str(ticket_id))
	
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
	
@put('/action/forward/<ticket_id:int>')
def on_action_forward(ticket_id):
	print("forward:"+str(ticket_id))
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'forward',
        request.query.email, user_auth.get_email_from_id(o)
    )
	
@put('/action/interrupted/<ticket_id:int>')
def on_action_interrupted(ticket_id):
	print("interrupted:"+str(ticket_id))
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'interrupted',
        request.query.email,
		user_auth.get_email_from_id(o)
    )

@put('/action/priority/increase/<ticket_id:int>')
def on_action_increase_priority(ticket_id):
	print("increase_priority:"+str(ticket_id))
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'increase_priority',
        request.query.email,
		user_auth.get_email_from_id(o)
    )
	
@put('/action/priority/decrease/<ticket_id:int>')
def on_action_decrese_priority(ticket_id):
	print("decrese_priority:"+str(ticket_id))
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'decrease_priority',
        request.query.email,
		user_auth.get_email_from_id(o)
    )

@put('/action/stalled/<ticket_id:int>')
def on_action_stalled(ticket_id):
	print("stalled:"+str(ticket_id))
	ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'stalled',
        request.query.email,
		user_auth.get_email_from_id(o)
    )
