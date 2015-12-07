#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Logic Box @2015
# This file contains several functions that do several operations necessary to this package to work
#

import new_ditic_kanban.tools
import new_server


from bottle import put
from bottle import get
from bottle import post
from bottle import template
from bottle import request
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file


	
@put('/action/backward/<ticket_id:int>')
def on_action_backward(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@put('/action/forward/<ticket_id:int>')
def on_action_forward(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@put('/action/interrupted/<ticket_id:int>')
def on_action_interrupted(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@put('/action/priority/increase/<ticket_id:int>')
def on_action_increase_priority(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@put('/action/priority/decrease/<ticket_id:int>')
def on_action_decrease_priority(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@put('/action/stalled/<ticket_id:int>')
def on_action_stalled(ticket_id):
    start_time = time()

    action = ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(o)
        ),
        ticket_id,
        'back',
        request.query.email, user_auth.get_email_from_id(o)
    )
    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}

@post('/ticket')
def new_ticket():
    start_time = time()

    new_ticket_data = request.body.read().split('\n')

    # Apply the action to the ticket
    create_ticket(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ),
        new_ticket_data[0],
        new_ticket_data[1],
        user_auth.get_email_from_id(request.query.o)
    )

    timespent = {'time_spent': '%0.2f seconds' % (time() - start_time)}
