#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# Kanban Logic for the GSIIC-DITIC environment
#


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
    email_limit = config.get_email_limits(ticket['owner'])
    actions = {
        'back': False,
        'forward': False,
        'increase_priority': False,
        'decrease_priority': False,
        'stalled': False,
        'interrupted': False,
    }

    # If UNKNOWN then don't allow nothing...
    if email == 'unknown':
        # If this is unknown, then allow nothing...
        pass

    # DIR-INBOX is very special...
    elif email == 'dir-inbox':
        actions['back'] = True
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

    # DIR is very special...
    elif email == 'dir':
        actions['increase_priority'] = True
        actions['decrease_priority'] = True
        actions['forward'] = True

    # If we are at IN (new), then we can move back or forward
    elif ticket['status'] == 'new':
        actions['back'] = True
        actions['increase_priority'] = True
        actions['decrease_priority'] = True
        status = 'open'
        if status in email_limit and status in number_tickets_per_status:
            if number_tickets_per_status[status] < email_limit[status]:
                actions['forward'] = True
        else:
            actions['forward'] = True

    # Here we will analyze the condition of ACTIVE (open)
    elif ticket['status'] == 'open':
        actions['stalled'] = True
        actions['interrupted'] = True
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        # Can we move back?
        status = 'new'
        if status in email_limit and status in number_tickets_per_status:
            if number_tickets_per_status[status] < email_limit[status]:
                actions['back'] = True
        else:
            actions['back'] = True

        # Can we move forward?
        status = 'rejected'
        if status in email_limit and status in number_tickets_per_status:
            if number_tickets_per_status[status] < email_limit[status]:
                actions['forward'] = True
        else:
            actions['forward'] = True

    # What about the STALLED? What can we do?
    elif ticket['status'] == 'stalled':
        actions['increase_priority'] = True
        actions['decrease_priority'] = True

        # Can we move back?
        status = 'open'
        if status in email_limit and status in number_tickets_per_status:
            if number_tickets_per_status[status] < email_limit[status]:
                actions['back'] = True
        else:
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
        else:
            actions['back'] = True

    ticket.update({'kanban_actions': actions})
    return
