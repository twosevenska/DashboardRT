# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This module is responsible for web routing. This is the main web server.
#
from time import time
from time import sleep
from datetime import date
import os
import threading
import pprint

from bottle import get
from bottle import post
from bottle import delete
from bottle import template
from bottle import request
from bottle import response
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file

from ditic_kanban.statistics import stats_update_json_file
from ditic_kanban.rt_summary import generate_summary_file
from ditic_kanban.rt_summary import get_summary_info
from ditic_kanban.config import DITICConfig
from ditic_kanban.auth import UserAuth
from ditic_kanban.tools import user_tickets_details
from ditic_kanban.tools import ticket_actions
from ditic_kanban.tools import user_closed_tickets
from ditic_kanban.tools import search_tickets
from ditic_kanban.tools import get_urgent_tickets
from ditic_kanban.tools import create_ticket
from ditic_kanban.rt_api import RTApi
from ditic_kanban.rt_api import fetch_ticket_details
from ditic_kanban.rt_api import fetch_ticket_brief_history
from ditic_kanban.rt_api import fetch_history_item
from ditic_kanban.statistics import get_date
from ditic_kanban.statistics import get_statistics


# My first global variable...
user_auth = UserAuth()

# Only used by the URGENT tickets search
my_config = DITICConfig()
system = my_config.get_system()
rt_object = RTApi(system['server'], system['username'], system['password'])

# This part is necessary in order to get access to sound files
# Static dir is in the parent directory
STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
print STATIC_PATH

# This variable set a the period between
# which the summaries are generated, in seconds
DELAY_BETWEEN_SUMMARIES = 60
# This flag is to stop the summary generation
exitFlag = False

pp = pprint.PrettyPrinter(indent=2)


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


################################################################
#   ROUTES
################################################################

@route('/')
def get_root():
    user_id = request.get_cookie('account', secret='secret')
    if user_id :
        redirect('/detail')
    else:
        redirect('/login')


@route('/login')
def get_login():
    return template('login', {})


@route('/detail')
def get_detail():
    user_id = request.get_cookie('account', secret='secret')
    if user_id:
        if user_id in user_auth.ids.keys():
            result = create_default_result()
            result.update({'username': user_auth.get_email_from_id(user_id)})
            result.update({'email': user_auth.get_email_from_id(user_id)})
            result.update({'username_id': user_id})

            result.update(user_tickets_details(
                user_auth.get_rt_object_from_email(
                    user_auth.get_email_from_id(user_id)
                 ), user_auth.get_email_from_id(user_id)))

            result.update(user_tickets_details(
                user_auth.get_rt_object_from_email(
                    user_auth.get_email_from_id(user_id)
                ), 'dir-inbox'))
            
            return template('detail', result)
        else:
    	    del_auth()
    	    redirect('/detail')
    else:
        redirect('/login')


################################################################
#   REST API
################################################################

@post('/auth')
def auth():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
    except AttributeError as e:
        print("AttributeError=" + str(e))
        response.status = 500
        return

    if username and password:
        try:
            if user_auth.check_password(username, password):
                user_id = user_auth.get_email_id(username)
                print('user_id=' + user_id)
                response.set_cookie('account', user_id, secret='secret')
                response.status = 200
            else:
                response.status = 401

        except ValueError as e:
            print("ValueError=" + str(e))
            response.status = 500
    else:
        response.status = 400


@delete('/auth')
def del_auth():
    user_id = request.get_cookie('account', secret='secret')
    if user_id :
        response.set_cookie('account', '', secret='secret')
        response.status = 200
    else:
        response.status = 204


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


@get('/closed/<email>')
def email_detail(email):
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': email})
    result.update({'username_id': request.query.o})

    result.update(user_closed_tickets(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), email))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('ticket_list', result)


@post('/search')
def search():
    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    if not request.forms.get('search'):
        redirect('/?o=%s' % request.query.o)
    search = request.forms.get('search')

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': search})
    result.update({'username_id': request.query.o})

    result.update(search_tickets(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), search))

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    return template('search', result)


@get('/ticket/<ticket_id>/action/<action>')
def ticket_action(ticket_id, action):

    start_time = time()

    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    # Apply the action to the ticket
    result.update(ticket_actions(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ),
        ticket_id,
        action,
        request.query.email, user_auth.get_email_from_id(request.query.o)
    ))

    # Update table for this user
    result.update(user_tickets_details(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), request.query.email))

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': request.query.email})
    result.update({'username_id': request.query.o})

    # Is there any URGENT ticket?
    result.update({'urgent': get_urgent_tickets(rt_object)})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    if request.query.email == 'dir' or request.query.email == 'dir-inbox' or request.query.email == 'unknown':
        return template('ticket_list', result)
    else:
        return template('detail', result)


@post('/ticket')
def new_ticket():
    start_time = time()
    result = create_default_result()
    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    new_ticket_data = request.body.read().split('\n')

    # Apply the action to the ticket
    result.update(create_ticket(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ),
        new_ticket_data[0],
        new_ticket_data[1],
        user_auth.get_email_from_id(request.query.o)
    ))

    # Update table for this user
    result.update(user_tickets_details(
        user_auth.get_rt_object_from_email(
            user_auth.get_email_from_id(request.query.o)
        ), request.query.email))

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'email': request.query.email})
    result.update({'username_id': request.query.o})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})
    if request.query.email == 'dir' or request.query.email == 'dir-inbox' or request.query.email == 'unknown':
        return template('ticket_list', result)
    else:
        return template('detail', result)


@get('/ticket/<ticket_id:int>')
def get_ticket_details(ticket_id):
    start_time = time()

    result = {'title': 'Ticket details'}

    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'username_id': request.query.o})

    result.update({'ticket_id': ticket_id})

    rt_api = user_auth.get_rt_object_from_email(user_auth.get_email_from_id(request.query.o))
    details = fetch_ticket_details(rt_api, ticket_id)
    pp.pprint(details)
    result.update(details)

    history = fetch_ticket_brief_history(rt_api, ticket_id)
    pp.pprint(history)
    result.update({'history': history})

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})

    return template('ticket_details', result)


@get('/ticket/<ticket_id:int>/history/<item_id:int>')
def get_history_item_details(ticket_id, item_id):
    start_time = time()

    result = {'title': 'Ticket #{tid}, history item #{iid}'.format(tid=ticket_id, iid=item_id)}

    if request.query.o == '' or not user_auth.check_id(request.query.o):
        result.update({'message': ''})
        return template('auth', result)

    result.update({'username': user_auth.get_email_from_id(request.query.o)})
    result.update({'username_id': request.query.o})

    result.update({'ticket_id': ticket_id})
    result.update({'item_id': item_id})

    rt_api = user_auth.get_rt_object_from_email(user_auth.get_email_from_id(request.query.o))
    details = fetch_history_item(rt_api, ticket_id, item_id)
    pp.pprint(details)
    result.update(details)

    result.update({'time_spent': '%0.2f seconds' % (time() - start_time)})

    return template('history_item_details', result)


@route("/static/<filepath:path>", name="static")
def static(filepath):
    return static_file(filepath, root=STATIC_PATH)


class SummaryGenerator(threading.Thread):
    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.delay = delay

    def run(self):
        while True:
            # if exitFlag:
                # self.exit()
            sleep(self.delay)

            generate_summary_file()
            sleep(self.delay)
            stats_update_json_file()
            print("generating summary...")


def start_server():
    generate_summary_file()
    SummaryGenerator(5).start()
    run(server='paste', host='0.0.0.0', debug=True)
