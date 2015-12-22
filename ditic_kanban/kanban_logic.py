#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# Kanban Logic for the GSIIC-DITIC environment
#

import rt_summary
import pprint

def create_ticket_possible_actions(config, ticket, email, number_tickets_per_status):
    """
    This function will create a dictionary with possible actions to be done to this ticket. It will be added to the
    ticket dictionary.
    Those actions will be used for determining if this ticket can be moved to other column

    :param config: the DITICConfig object
    :param ticket: a dictionary with the ticket values
    :param number_tickets_per_status: the number of tickets (used to evaluate if this ticket can be moved)
    :return: Null
    """
    pp = pprint.PrettyPrinter(indent=2)
    email_limit = config.get_email_limits(ticket['owner'])
    actions = {
        'back': False,
        'forward': False,
        'increase_priority': False,
        'decrease_priority': False,
        'stalled': False,
        'interrupted': False,
        'take': False,
    }

    # If UNKNOWN then don't allow nothing...
    if email == 'unknown':
        # If this is unknown, then allow nothing...
        pass

    # DIR is very special...(no-limit)
    elif email == 'dir':
        actions['increase_priority'] = True
        actions['decrease_priority'] = True
        #Urgent is like God status
        if ticket['cf.{ditic-urgent}'] == 'yes':
            actions['forward'] = True
        else:
            # Can we move forward?
            status='new'
            email_limit = config.get_email_limits('dir-inbox')

            soma = 0
            summary = rt_summary.get_summary_info()
            
            for status in summary['dir-inbox']:
                soma += summary['dir-inbox'][status]
            pp.pprint(summary['dir-inbox'])
            if status in email_limit and status in number_tickets_per_status:
                if soma < email_limit['dir-inbox']:
                    actions['forward'] = True
            
            

    # DIR-INBOX is very special...(shared by all)
    elif email == 'dir-inbox':
        actions['back'] = True
        actions['increase_priority'] = True
        actions['decrease_priority'] = True
        #Urgent is like God status
        if ticket['cf.{ditic-urgent}'] == 'yes':
            actions['take'] = True
        else:
            # Can we take ticket?
            email = 'dir-inbox'
            email_limit = config.get_email_limits(email)
            status = 'new'
            
            soma = 0
            summary = rt_summary.get_summary_info()
            for status in summary['dir-inbox']:
                soma += summary['dir-inbox'][status]
            if status in email_limit and status in number_tickets_per_status:
                if number_tickets_per_status[status] < email_limit[status]:
                    actions['take'] = True
            

    # If we are at IN (new), then we can move back or forward
    elif ticket['status'] == 'new':

        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        #Urgent is like God status
        if ticket['cf.{ditic-urgent}'] == 'yes':
            actions['back'] = True
            actions['forward'] = True
        else:
            # Can we move back?
            status = 'new'
            email = 'dir-inbox'
            soma = 0
            summary = rt_summary.get_summary_info()
            for status in summary['dir-inbox']:
                soma += summary['dir-inbox'][status]
            if status in email_limit and status in number_tickets_per_status:
                if soma < email_limit['dir-inbox']:
                    actions['back'] = True
            

            # Can we move forward?
            status = 'open'
            if status in email_limit and status in number_tickets_per_status:
                if number_tickets_per_status[status] < email_limit[status]:
                    actions['forward'] = True
            

    # Here we will analyze the condition of ACTIVE (open)
    elif ticket['status'] == 'open':
        actions['stalled'] = True
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        #Urgent is like God status
        if ticket['cf.{ditic-urgent}'] == 'yes':
            actions['interrupted'] = True
            actions['forward'] = True
        else:

            # Can we move back?
            status = 'new'
            if status in email_limit and status in number_tickets_per_status:
                if number_tickets_per_status[status] < email_limit[status]:
                    actions['interrupted'] = True
            

            # Can we move forward?
            status = 'rejected'
            if status in email_limit and status in number_tickets_per_status:
                if number_tickets_per_status[status] < email_limit[status]:
                    actions['forward'] = True
            

    # What about the STALLED? What can we do?
    elif ticket['status'] == 'stalled':
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        #Urgent is like God status
        if ticket['cf.{ditic-urgent}'] == 'yes':
            actions['back'] = True

        else:
            # Can we move back?
            status = 'new'
            if status in email_limit and status in number_tickets_per_status:
                if number_tickets_per_status[status] < email_limit[status]:
                    actions['back'] = True
           

    # Ready to RT actions
    elif ticket['status'] == 'rejected':
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        # Can we move back?
        status = 'open'
        if status in email_limit and status in number_tickets_per_status:
            if number_tickets_per_status[status] < email_limit[status]:
                actions['back'] = True
        

    ticket.update({'kanban_actions': actions})
    return
