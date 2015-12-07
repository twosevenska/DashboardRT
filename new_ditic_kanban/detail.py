#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Logic Box @2015
# This module is responsible for information related to the user.

from bottle import get
from time import time
from new_server import create_default_result

@get('/detail/<email>')
def email_detail(email):
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': email})
    result.update({'username_id': request.query.o})

    result.update(user_tickets_details(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), email))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    if email == 'dir' or email == 'dir-inbox' or email == 'unknown':
        return template('ticket_list', result)
    else:
        return template('detail', result)