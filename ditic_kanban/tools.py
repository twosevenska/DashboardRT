#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
from time import time
from time import ctime
from time import mktime
from time import strptime
from datetime import date
from datetime import timedelta
import pprint

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api import get_list_of_tickets
from ditic_kanban.rt_api import modify_ticket
from ditic_kanban.rt_api import create_new_ticket
from ditic_kanban.rt_api import comment_ticket
from ditic_kanban.kanban_logic import create_ticket_possible_actions
import rt_summary


def group_result_by(data, order_by):
    """
    This function will create a dictionary ordering values by the order_by value.
    List example:
        [
            {
                'key1': 'value1',
                'key2': 'value2',
                ...
            }
            ...
        ]

    Result example:
        {'value1':
            [
                {
                    'key1': 'value1',
                    'key2': 'value2',
                    ...
                },
                ...
            ]
         ...
        }

    :param data: a list
    :param order_by: a string. This value will be used to generate output. All values not found will
                    be associated to a value 'unknown'
    :return: a dictionary
    """
    result = dict()
    for line in data:
        # By default, we don't know to whom this belongs
        value = 'unknown'
        if order_by in line:
            value = line[order_by]

        # If there is no entry with that value, then create it
        if value not in result:
            result[value] = []

        # Add this line to this value
        result[value].append(line)

    return result


def user_tickets_details(rt_object, email, requestor_email=None):
    """
    Returns the list of tickets for a user/email

    :param rt_object: rt object for querying (must be users authenticated)
    :param email: the user email

    :return: a dictionary
    """

    query = 'Owner = "'+email+'" AND Queue = "general" '
    pp = pprint.PrettyPrinter(indent=2)
    config = DITICConfig()

    # If the user is dir, then build the search
    if email == 'dir':
        query = 'Queue = "general" AND "CF.{IS - Informatica e Sistemas}" = "DIR" AND Owner = "Nobody"  AND ' \
                'Status != "resolved" AND Status != "deleted" '

    # If the user is dir-inbox, then search for it
    elif email == 'dir-inbox':
        query = 'Queue = "general" AND "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" AND Owner = "Nobody"  AND ' \
                'Status != "resolved" AND Status != "deleted" '

    # If the user is unknown, then search all users but those that we already know
    elif email == 'unknown':
        query = 'Queue = "general" AND "CF.{IS - Informatica e Sistemas}" LIKE "DIR%"  AND ' \
                'Status != "resolved" AND Status != "deleted" '
        for user in config.get_email_to_user().keys():
            query += 'AND Owner != "'+user+'" '
        query += 'AND Owner != "Nobody"'

    # Otherwise, check if user is not known...
    elif not config.check_if_email_exist(email):
        raise ValueError('Unknown email/user:'+email)

    # Ok, if we got here, then the user exist
    # Status != "resolved" AND
    else:
        query += 'AND  (  Status != "deleted" )'

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query)
    except ValueError as e:
        response = []

    if email == 'unknown':
        number_tickets_per_status = {email: len(response)}
        result = group_result_by(response, 'priority')

        for priority in result:
            for line in result[priority]:
                create_ticket_possible_actions(config, line, email, number_tickets_per_status, requestor_email)

    elif email == 'dir' or email == 'dir-inbox':
        number_tickets_per_status = {email: len(response)}
        result = group_result_by(response, 'priority')
        if requestor_email or email == 'dir':
            if email == 'dir':
                query = 'Queue = "general" AND ' \
                        '"CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" AND Owner = "Nobody"  AND ' \
                        'Status != "resolved" AND Status != "deleted" '
                requestor_email = 'dir-inbox'

            else:
                query = 'Owner = "'+requestor_email+'" AND Queue = "general" AND  (  Status != "deleted" )'

            try:
                response = get_list_of_tickets(rt_object, query)
            except ValueError as e:
                response = []

            number_tickets_user_in = 0
            response_grouped_by_status = group_result_by(response, 'status')
            if 'new' in response_grouped_by_status:
                number_tickets_user_in = len(response_grouped_by_status['new'])

            for priority in result:
                for line in result[priority]:
                    create_ticket_possible_actions(config, line,
                                                   email, number_tickets_per_status,
                                                   requestor_email, number_tickets_user_in)
        else:
            number_tickets_per_status = {email: len(response)}
            result = group_result_by(response, 'priority')
            for priority in result:
                for line in result[priority]:
                    create_ticket_possible_actions(config, line, email, number_tickets_per_status, requestor_email)
    else:
        # Get some statistics
        response_grouped_by_status = group_result_by(response, 'status')
        number_tickets_per_status = {}
        for status in response_grouped_by_status:
            number_tickets_per_status[status] = len(response_grouped_by_status[status])

        result = {}
        for status in response_grouped_by_status:
            if status == 'new':
                query = 'Queue = "general" AND ' \
                        '"CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" AND Owner = "Nobody"  AND ' \
                        'Status != "resolved" AND Status != "deleted" '
                try:
                    response_dir_in = get_list_of_tickets(rt_object, query)
                except ValueError as e:
                    response_dir_in = []

                status_new = group_result_by(response_dir_in, 'status')
                number_tickets_dir_inbox=0
                if 'new' in status_new:
                    number_tickets_dir_inbox = len(status_new['new'])
                next_limit = 0
                if 'open' in number_tickets_per_status:
                    next_limit = number_tickets_per_status['open']

                grouped_by_priority = group_result_by(response_grouped_by_status[status], 'priority')
                result[status] = grouped_by_priority
                for priority in grouped_by_priority:
                    for line in grouped_by_priority[priority]:
                        create_ticket_possible_actions(config, line,
                                                       email, number_tickets_per_status,
                                                       'dir-inbox', number_tickets_dir_inbox, next_limit)
            else:
                grouped_by_priority = group_result_by(response_grouped_by_status[status], 'priority')

                result[status] = grouped_by_priority
                for priority in grouped_by_priority:
                    for line in grouped_by_priority[priority]:

                        create_ticket_possible_actions(config, line, email, number_tickets_per_status)

    # The user limits...
    email_limit = config.get_email_limits(email)

    return {
        'tickets': result,
        'number_tickets_per_status': number_tickets_per_status,
        'email_limit': email_limit,
    }


# noinspection PyArgumentList
def calculate_time_worked(ticket_line):
    """
    Receives a ticket line in the format explained in the RTApi -> get_list_of_tickets.
    It will return an int with the total number of time worked.

    It MUST exist the variables
        ticket_line['timeworked']
        ticket!'starts']

    :param ticket_line: A dictionary with RT values
    :return: an int with the time worked on this ticket
    """
    last_time_worked = ticket_line['timeworked']
    if last_time_worked.find(' minutes') > 0:
        last_time_worked = int(last_time_worked[:last_time_worked.find(' minutes')])
    elif last_time_worked.find(' hours') > 0:
        last_time_worked = int(last_time_worked[:last_time_worked.find(' hours')])*60
    else:
        last_time_worked = 0
    try:
        time_spent_now = (time()-mktime(strptime(ticket_line['starts'])))/60
    except ValueError:
        time_spent_now = 0
    if time_spent_now > 540:
        time_spent_now = 0

    return str(time_spent_now + last_time_worked)


def ticket_actions(rt_object, ticket_id, action, ticket_email, user_email):
    """
    In this function we will apply the ticket action requested by user.
    It is possible to change the ticket priority, owner, etc.

    :param rt_object: rt object for querying (must be users authenticated)
    :param ticket_id: The ticket we want to see possible actions
    :param action: the action requested.
    :param ticket_email: The ticket owner (we need this because of the special user dir, dir-inbox and unknown)
    :param user_email: the user email who is requesting this action (we need this to take a ticket)
    :return: RT result (I think we must change this output!)
    """
    # First of all, get the actual ticket information
    query = 'id = "%s"' % ticket_id

    # Get the information from the server.
    try:
        ticket_line = get_list_of_tickets(rt_object, query)[0]
    except NameError as e:
        return 'Error:'+str(e)

    # There is so much to be done. So this is the default answer.
    result = 'Still working on it... sorry for the inconvenience!'
    message = ''

    if '-' in action:
        action_and_message = get_ticket_action_and_message(action)
        message = action_and_message[1]
        action = action_and_message[0]
    print message
    # INCREASE PRIORITY ##############################
    if action == 'increase_priority':
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'priority': str(int(ticket_line['priority']) + 1)
            }
        )

    # DECREASE PRIORITY ##############################
    elif action == 'decrease_priority':
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'priority': str(int(ticket_line['priority']) - 1)
            }
        )

    # BACK ##############################
    elif action == 'back':
        if ticket_email == 'dir-inbox':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'cf.{is - informatica e sistemas}': 'dir',
                }
            )
        elif ticket_line['status'] == 'new':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'owner': 'nobody',
                    'cf.{is - informatica e sistemas}': 'dir-inbox',
                }
            )
        elif ticket_line['status'] == 'open':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'timeworked': calculate_time_worked(ticket_line) + ' minutes',
                    'starts': '0',
                    'status': 'new'
                }
            )
        elif ticket_line['status'] == 'rejected':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'starts': ctime(time()),
                    'status': 'open',
                }
            )
        elif ticket_line['status'] == 'stalled':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'starts': ctime(time()),
                    'status': 'new',
                }
            )

    # FORWARD ##############################
    elif action == 'forward':
        if ticket_email == 'dir':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'cf.{is - informatica e sistemas}': 'dir-inbox',
                }
            )
        elif ticket_line['status'] == 'new':

            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'starts': ctime(time()),
                    'status': 'open',
                }
            )

        elif ticket_line['status'] == 'open':
            if message:
                comment_the_ticket(rt_object, ticket_id, "conclusion text:"+message)
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'timeworked': calculate_time_worked(ticket_line) + ' minutes',
                    'starts': '0',
                    'status': 'resolved'
                }
            )

    # STALLED ##############################
    elif action == 'stalled':
        if ticket_line['status'] == 'open':
            result = modify_ticket(
                rt_object,
                ticket_id,
                {
                    'timeworked': calculate_time_worked(ticket_line) + ' minutes',
                    'starts': '0',
                    'status': 'stalled',
                }
            )

    # TAKE ##############################
    elif action == 'take':
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'owner': user_email,
            }
        )

    # URGENT ##############################
    elif action == 'set_urgent':
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'cf.{DITIC-Urgent}': 'yes',
            }
        )
    elif action == 'unset_urgent':
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'cf.{DITIC-Urgent}': '',
            }
        )

    # Interrupted ##############################
    elif action == 'interrupted':
        if ticket_line['cf.{ditic-interrupted}']:
            interrupted = int(ticket_line['cf.{ditic-interrupted}']) + 1
        else:
            interrupted = 1
        result = modify_ticket(
            rt_object,
            ticket_id,
            {
                'cf.{DITIC-Interrupted}': str(interrupted),
            }
        )
        return ticket_actions(rt_object, ticket_id, 'back', ticket_email, user_email)

    return {
        'action_result': result
    }


def create_ticket(rt_object, subject, text, user_email):
    """
    Creates a ticket in rt

    :param rt_object: rt object for querying (must be users authenticated)
    :param subject: the subject of the new ticket
    :param text: description of a ticket
    :param user_email: the email of the user requesting the ticket creation

    :return: a dictionary
    """
    result = create_new_ticket(
        rt_object,
        {
            'Queue': 'general',
            'Requestor': user_email,
            'Subject': subject,
            'Cc': '',
            'AdminCc': '',
            'Owner': 'nobody',
            'Status': 'new',
            'Priority': '25',
            'InitialPriority': '25',
            'FinalPriority': '',
            'TimeEstimated': '',
            'Starts': '',
            'Due': '',
            'Text': text,
            'cf.{is - informatica e sistemas}': 'dir'
        }
    )

    return {
        'action_result': result
    }


def comment_the_ticket(rt_object, ticket_id, text):
    """
    Adds a comment to a ticket

    :param rt_object: rt object for querying (must be users authenticated)
    :param ticket_id: The Id of the ticket
    :param text: body of the comment

    :return: a dictionary
    """
    result = comment_ticket(
        rt_object,
        ticket_id,
        {
            'id': ticket_id,
            'Action': 'comment',
            'Text': text
        }
    )

    return {
        'action_result': result
    }


def get_ticket_action_and_message(action):
    """
    This simply splits the action and it's text received from the browser

    :param action: a ticket action

    :return: a list
    """
    # TODO: This was just a temporary solution. The whole thing should be done with JSONS

    if '-' not in action:
        return action
    result = action.split("-")
    
    try:
        result[1] = result[1].replace("_", " ")
    except IndexError:
        pass
    return result


# noinspection PyArgumentList
def user_closed_tickets(rt_object, email):
    """
    Get the closed tickets on the last X days. (X = 60)

    :param rt_object: RTApi object
    :param email: the user email (it must exist in the config)
    :return:
    """
    config = DITICConfig()

    # Check if user is known...
    if not config.check_if_email_exist(email):
        raise ValueError('Unknown email/user:'+email)

    # Search last 30 days.
    previous_date = (date.today() - timedelta(60)).isoformat()

    # The search string
    query = 'Owner = "%s" AND Queue = "general" AND  Status = "resolved" AND LastUpdated > "%s"' % (email,
                                                                                                    previous_date)

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query)
    except NameError as e:
        raise ValueError('Error: '+str(e))

    number_tickets_per_status = {email: len(response)}
    for line in response:
        try:
            auxiliary_date = strptime(line['lastupdated'])
            auxiliary_date = '%02d/%02d' % (auxiliary_date.tm_mon, auxiliary_date.tm_mday)
        except ValueError:
            auxiliary_date = 0
        line['auxiliary_date'] = auxiliary_date
        create_ticket_possible_actions(config, line, email, number_tickets_per_status)
    result = group_result_by(response, 'auxiliary_date')

    email_limit = config.get_email_limits(email)

    return {
        'tickets': result,
        'number_tickets_per_status': number_tickets_per_status,
        'email_limit': email_limit,
    }


# noinspection PyArgumentList
def search_tickets(rt_object, search):
    """
    Search for tickets that match those criteria.
    The search will focus on those fields:
        - Requestors.EmailAddress
        - Subject
        - cf{servico}
        - cc
        - admincc
        - Requestor.Name
        - Requestor.RealName

    The tickets must be under the following restrictions:
        - Belongs to Queue General
        - Must have "CF.{IS - Informatica e Sistemas}" equal to DIR or DIR-INBOX
        - Must be created or updated on the last 90 days

    :param rt_object: RTApi object
    :param search: the search criteria
    :return:
    """
    config = DITICConfig()

    # Search last 30 days.
    previous_date = (date.today() - timedelta(90)).isoformat()

    # The search string
    query = 'Queue = "General" AND ( "CF.{IS - Informatica e Sistemas}" = "DIR" ' \
            'OR "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" ) AND ' \
            '( Lastupdated > "'+previous_date+'" OR Created > "'+previous_date+'") ' \
            'AND ( Requestor.EmailAddress LIKE "%'+search+'%" '
    for query_items in ['Subject', 'cf.{servico}', 'cc', 'admincc', 'Requestor.Name', 'Requestor.RealName']:
        query += ' OR %s LIKE "%%%s%%" ' % (query_items, search)
    query += ')'

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query)
    except NameError as e:
        raise ValueError('Error: '+str(e))
    except ValueError:
        return {
            'no_result': True,
            'number_tickets': 'No results...',
            'tickets': {},
        }

    number_tickets = len(response)
    for line in response:
        try:
            auxiliary_date = strptime(line['lastupdated'])
            auxiliary_date = '%02d/%02d' % (auxiliary_date.tm_mon, auxiliary_date.tm_mday)
        except ValueError:
            auxiliary_date = 0
        line['auxiliary_date'] = auxiliary_date
    result = group_result_by(response, 'auxiliary_date')

    email_limit = config.get_email_limits(search)

    return {
        'no_result': False,
        'tickets': result,
        'number_tickets': number_tickets,
        'email_limit': email_limit,
    }


def get_number_of_tickets(rt_object, query):
    """
    This function will return the number of tickets that matches the query.

    :param rt_object: the RTApi object for querying
    :param query: the query
    :return: the number of tickets found
    """
    # Just a simple check... ;)
    if query == '':
        return 0

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query, detail=False)
    except ValueError:
        return 0

    return len(response)


def get_urgent_tickets(rt_object):
    """
    This function will return the list of urgent tickets.
    To be an urgent ticket it must:
    - Be in the DIR-INBOX
    - Have status 'new'
    - Have the cf.{ditic-urgent} == yes


    :param rt_object:
    :return:
    """
    query = '"cf.{is - informatica e sistemas}" = "dir-inbox" AND "cf.{ditic-urgent}" = "yes"' \
            'AND Owner = "nobody"'

    # Get the information from the server.
    try:
        return get_list_of_tickets(rt_object, query, detail=False)
    except ValueError:
        return []


def get_dir_inbox_num():
    """
    Get the total number of tickets in dir-inbox

    :return: A number
    """
    summary = rt_summary.get_summary_info()
    total = 0
    for status in summary['dir-inbox']:
        total += summary['dir-inbox'][status]
    return total


def archive_all_tickets(rt_object, email):
    """
    Archives all tickets associated with a user

    :param rt_object: rt object for querying (must be users authenticated)
    :param email: The user email

    """
    response = user_closed_tickets_simple(rt_object, email)

    for ticket in response:
        archive_the_ticket(rt_object, ticket['id'])


def archive_the_ticket(rt_object, ticket_id):
    """
    Archive a ticket

    :param rt_object: rt object for querying (must be users authenticated)
    :param ticket_id: The Id of the ticket

    :return: a dictionary
    """
    result = modify_ticket(
        rt_object,
        ticket_id,
        {
            'Status': 'deleted',
        }
    )

    return {
        'action_result': result
    }


# noinspection PyArgumentList
def user_closed_tickets_simple(rt_object, email):
    """
    Gets the closed tickets of a user

    :param rt_object: RTApi object
    :param email: the user email (it must exist in the config)
    :return: A dictionary
    """
    config = DITICConfig()

    # Check if user is known...
    if not config.check_if_email_exist(email):
        raise ValueError('Unknown email/user:'+email)

    # The search string
    query = 'Owner = "%s" AND Queue = "general" AND  Status = "resolved"' % (email)

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query)
    except NameError as e:
        raise ValueError('Error: '+str(e))

    return response
