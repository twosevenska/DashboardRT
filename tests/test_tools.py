#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
from time import time
from time import ctime

import pytest

from ditic_kanban.config import DITICConfig

from ditic_kanban.tools import group_result_by
from ditic_kanban.tools import user_tickets_details
from ditic_kanban.tools import calculate_time_worked
from ditic_kanban.tools import ticket_actions
from ditic_kanban.tools import user_closed_tickets
from ditic_kanban.tools import search_tickets
from ditic_kanban.tools import get_number_of_tickets
from ditic_kanban.tools import get_urgent_tickets

from mock_rt_api import RTApiMock


def test_group_result_by_known_parameter():
    data = [
        {
            'owner': 'vapi@uc.pt',
            'status': 'open',
        },
        {
            'owner': 'asantos@uc.pt',
            'status': 'resolved',
        },
    ]
    result = group_result_by(data, 'owner')
    assert result == {
        'vapi@uc.pt': [
            {
                'owner': 'vapi@uc.pt',
                'status': 'open',
            }
        ],
        'asantos@uc.pt': [
            {
                'owner': 'asantos@uc.pt',
                'status': 'resolved',
            }
        ],
    }

def test_group_result_by_unknown_parameter():
    data = [
        {
            'owner': 'vapi@uc.pt',
            'status': 'open',
        },
        {
            'owner': 'asantos@uc.pt',
            'status': 'resolved',
        },
    ]
    result = group_result_by(data, 'not_known')
    assert result == {
        'unknown': [
            {
                'owner': 'vapi@uc.pt',
                'status': 'open',
            },
            {
                'owner': 'asantos@uc.pt',
                'status': 'resolved',
            },
        ],
    }

def test_user_tickets_details_known_email():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
    ])
    result = user_tickets_details(rt_object, 'vapi@uc.pt')
    assert result == {
        'email_limit':
            {
                'new': 7,
                'open': 1,
                'rejected': 7
            },
        'number_tickets_per_status':
            {
                u'open': 1
            },
        'tickets':
            {
                u'open':
                    {
                        u'26':
                            [
                                {
                                    u'cf.{is - informatica e sistemas}': u'dir-inbox',
                                    u'cf.{servico}': u'csc-gsiic',
                                    'id': u'887677',
                                    'kanban_actions':
                                        {
                                            'back': True,
                                            'decrease_priority': True,
                                            'forward': True,
                                            'increase_priority': True,
                                            'interrupted': True,
                                            'stalled': True
                                        },
                                    u'owner': u'vapi@uc.pt',
                                    u'priority': u'26',
                                    u'status': u'open',
                                    u'subject': u'create rt dashboard'
                                }
                            ]
                    }
            }
    }

def test_user_tickets_details_unknown_email():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
    ])
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    with pytest.raises(ValueError) as value_error:
        user_tickets_details(rt_object, 'unknown@uc.pt')
    assert 'Unknown email/user:' in str(value_error)

def test_user_tickets_details_dir():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: nobody',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir',
    ])
    result = user_tickets_details(rt_object, 'dir')
    assert rt_object.data == {
        'query': 'Queue = "general" AND "CF.{IS - Informatica e Sistemas}" = "DIR" '
                 'AND Owner = "Nobody"  AND Status != "resolved" AND Status != "deleted" ',
        'format': 'l'
    }
    assert result == {
        'tickets':
            {
                u'26':
                    [
                        {
                            u'status': u'open',
                            u'priority': u'26',
                            'kanban_actions':
                                {
                                    'increase_priority': True,
                                    'decrease_priority': True,
                                    'back': False,
                                    'interrupted': False,
                                    'stalled': False,
                                    'forward': True
                                },
                            u'owner': u'nobody',
                            u'cf.{is - informatica e sistemas}': u'dir',
                            u'id': u'887677',
                            u'cf.{servico}': u'csc-gsiic',
                            u'subject': u'create rt dashboard'
                        }
                    ]
            },
        'email_limit': {},
        'number_tickets_per_status':
            {
                'dir': 1
            }
    }

def test_user_tickets_details_dir_inbox():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: nobody',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
    ])
    result = user_tickets_details(rt_object, 'dir-inbox')
    assert rt_object.data == {
        'query': 'Queue = "general" AND "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" '
                 'AND Owner = "Nobody"  AND Status != "resolved" AND Status != "deleted" ',
        'format': 'l'
    }
    assert result == {
        'tickets':
            {
                u'26':
                    [
                        {
                            u'status': u'open',
                            u'priority': u'26',
                            'kanban_actions':
                                {
                                    'increase_priority': True,
                                    'decrease_priority': True,
                                    'back': True,
                                    'interrupted': False,
                                    'stalled': False,
                                    'forward': False
                                },
                            u'owner': u'nobody',
                            u'cf.{is - informatica e sistemas}': u'dir-inbox',
                            u'id': u'887677',
                            u'cf.{servico}': u'csc-gsiic',
                            u'subject': u'create rt dashboard'
                        }
                    ]
            },
        'email_limit': {},
        'number_tickets_per_status':
            {
                'dir-inbox': 1
            }
    }

def test_user_tickets_details_unknown():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: something@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    result = user_tickets_details(rt_object, 'unknown')
    assert 'Owner != "Nobody"' in rt_object.data['query']
    assert result == {
        'tickets':
            {
                u'26':
                    [
                        {
                            u'status': u'open',
                            u'priority': u'26',
                            'kanban_actions':
                                {
                                    'increase_priority': False,
                                    'decrease_priority': False,
                                    'back': False,
                                    'interrupted': False,
                                    'stalled': False,
                                    'forward': False
                                },
                            u'owner': u'something@uc.pt',
                            u'cf.{is - informatica e sistemas}': u'dir-inbox',
                            u'id': u'887677',
                            u'cf.{servico}': u'csc-gsiic',
                            u'subject': u'create rt dashboard'
                        }
                    ]
            },
        'email_limit': {},
        'number_tickets_per_status':
            {
                'unknown': 1
            }
    }

def test_calculate_time_worked_few_ms():
    data = {
        u'timeworked': u'10 minutes',
        u'starts': ctime(time()),
    }
    result = calculate_time_worked(data)
    assert '10.' in result

def test_calculate_time_worked_over_9_hours():
    data = {
        u'timeworked': u'10 minutes',
        u'starts': 'fri jul 24 13:08:34 2015',
    }
    result = calculate_time_worked(data)
    assert result == '10'

def test_ticket_actions_increase_priority():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'increase_priority', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'priority: 27\n'
    }

def test_ticket_actions_decrease_priority():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'decrease_priority', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'priority: 25\n'
    }

def test_ticket_actions_back_dir_inbox():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'back', 'dir-inbox', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'cf.{is - informatica e sistemas}: dir\n',
    }

def test_ticket_actions_back_new():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: new',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'back', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'owner: nobody\ncf.{is - informatica e sistemas}: dir-inbox\n',
    }

def test_ticket_actions_back_open():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'back', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: new\nstarts: 0\ntimeworked: 10.' in rt_object.data['content']

def test_ticket_actions_back_rejected():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: rejected',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'back', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: open\nstarts: ' in rt_object.data['content']

def test_ticket_actions_back_stalled():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: stalled',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'back', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: open\nstarts: ' in rt_object.data['content']

def test_ticket_actions_forward_dir():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: stalled',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'forward', 'dir', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'cf.{is - informatica e sistemas}: dir-inbox\n',
    }

def test_ticket_actions_forward_new():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: new',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'forward', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: open\nstarts: ' in rt_object.data['content']

def test_ticket_actions_forward_open():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'forward', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: rejected\nstarts: 0\ntimeworked: 10.' in rt_object.data['content']

def test_ticket_actions_stalled_open():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'starts: '+str(ctime(time())),
                u'timeworked: 10 minutes',
        ]
    )
    ticket_actions(rt_object, '887677', 'stalled', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert 'status: stalled\nstarts: 0\ntimeworked: 10.' in rt_object.data['content']

def test_ticket_actions_take():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'take', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'owner: vapi@uc.pt\nstatus: new\n',
    }

def test_ticket_actions_set_urgent():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'set_urgent', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'cf.{DITIC-Urgent}: yes\n',
    }


def test_ticket_actions_unset_urgent():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    ticket_actions(rt_object, '887677', 'unset_urgent', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.uri == 'ticket/887677/edit'
    assert rt_object.data == {
        'content': 'cf.{DITIC-Urgent}: \n',
    }


def test_ticket_actions_unknown_option():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
        ]
    )
    result = ticket_actions(rt_object, '887677', 'not_known', 'vapi@uc.pt', 'vapi@uc.pt')
    assert rt_object.data == {
        'query': 'id = "887677"',
        'format': 'l'
    }
    assert rt_object.uri == '/search/ticket'
    assert result == {
        'action_result': 'Still working on it... sorry for the inconvenience!'
    }

def test_user_closed_tickets_known_email():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'lastupdated: wed jul 15 21:16:50 2015',
    ])
    result = user_closed_tickets(rt_object, 'vapi@uc.pt')
    assert result == {
        'tickets':
            {
                '07/15':
                    [
                        {
                            u'status': u'open',
                            u'priority': u'26',
                            'kanban_actions':
                                {
                                    'increase_priority': True,
                                    'decrease_priority': True,
                                    'back': True,
                                    'interrupted': True,
                                    'stalled': True,
                                    'forward': True
                                },
                            u'lastupdated': u'wed jul 15 21:16:50 2015',
                            'auxiliary_date': '07/15',
                            u'owner': u'vapi@uc.pt',
                            u'cf.{is - informatica e sistemas}': u'dir-inbox',
                            'id': u'887677',
                            u'cf.{servico}': u'csc-gsiic',
                            u'subject': u'create rt dashboard'
                        }
                    ]
            },
        'email_limit':
            {
                'new': 7,
                'open': 1,
                'rejected': 7
            },
        'number_tickets_per_status':
            {
                'vapi@uc.pt': 1
            }
    }


def test_user_closed_tickets_unknown_email():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
    ])
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    with pytest.raises(ValueError) as value_error:
        user_closed_tickets(rt_object, 'unknown@uc.pt')
    assert 'Unknown email/user:' in str(value_error)


def test_search_tickets_With_result():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'lastupdated: wed jul 15 21:16:50 2015',
    ])
    result = search_tickets(rt_object, 'vapi@uc.pt')
    assert result == {
        'tickets':
            {
                '07/15':
                    [
                        {
                            u'status': u'open',
                            u'priority': u'26',
                            u'lastupdated': u'wed jul 15 21:16:50 2015',
                            'auxiliary_date': '07/15',
                            u'owner': u'vapi@uc.pt',
                            u'cf.{is - informatica e sistemas}': u'dir-inbox',
                            'id': u'887677',
                            u'cf.{servico}': u'csc-gsiic',
                            u'subject': u'create rt dashboard'
                        }
                    ]
            },
        'no_result': False,
        'number_tickets': 1,
        'email_limit':
            {
                'new': 7,
                'open': 1,
                'rejected': 7
            }
    }

def test_get_number_of_tickets_query_ok():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'rt/4.0.6 200 ok', u'',
                u'887677: create rt dashboard',
    ])
    result = get_number_of_tickets(rt_object, 'Owner = "vapi@uc.pt"')
    assert result == 1


def test_get_number_of_tickets_query_not_ok():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'rt/4.0.6 200 ok', u'',
                u'887677: create rt dashboard',
    ])
    result = get_number_of_tickets(rt_object, '')
    assert result == 0


def test_get_number_of_tickets_query_not_ok_raise_exception():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'rt/4.0.6 200 ok', u'',
                u'invalid query: just testing...',
    ])
    result = get_number_of_tickets(rt_object, 'Something')
    assert result == 0


def test_get_urgent_tickets():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'rt/4.0.6 200 ok', u'',
                u'81818: This is a test...',
    ])

    result = get_urgent_tickets(rt_object)
    assert result == [{'id': '81818', 'subject': 'This is a test...'}]
