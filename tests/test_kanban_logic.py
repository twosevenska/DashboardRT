#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
from ditic_kanban.kanban_logic import create_ticket_possible_actions

from mock_config import DITICConfigMock

def test_create_ticket_possible_actions_email_unknown():
    ticket = {
        'owner': 'email_unknown@uc.pt',
        'status': 'new',
    }
    email = 'unknown'
    config = DITICConfigMock()

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': False,
        'decrease_priority': False,
        'back': False,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_dir_inbox():
    ticket = {
        'owner': 'nobody',
        'status': 'new',
    }
    email = 'dir-inbox'
    config = DITICConfigMock()

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_dir():
    ticket = {
        'owner': 'nobody',
        'status': 'new',
    }
    email = 'dir'
    config = DITICConfigMock()

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': False,
        'interrupted': False,
        'stalled': False,
        'forward': True,
    }

def test_create_ticket_possible_actions_status_new_and_limit_ok():
    ticket = {
        'owner': 'nobody',
        'status': 'new',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 0,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': True,
    }

def test_create_ticket_possible_actions_user_vapi_status_new_and_limit_over():
    ticket = {
        'owner': 'vapi@uc.pt',
        'status': 'new',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_new_and_no_limit():
    ticket = {
        'owner': 'vapi@uc.pt',
        'status': 'new',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {}

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': True,
    }

def test_create_ticket_possible_actions_user_vapi_status_open_and_limit_ok():
    ticket = {
        'owner': 'nobody',
        'status': 'open',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 6,
        'open': 0,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': True,
        'stalled': True,
        'forward': True,
    }

def test_create_ticket_possible_actions_user_vapi_status_open_and_limit_over():
    ticket = {
        'owner': 'nobody',
        'status': 'open',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': False,
        'interrupted': True,
        'stalled': True,
        'forward': True,
    }

def test_create_ticket_possible_actions_user_vapi_status_open_and_no_limit():
    ticket = {
        'owner': 'nobody',
        'status': 'open',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {}

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': True,
        'stalled': True,
        'forward': True,
    }

def test_create_ticket_possible_actions_user_vapi_status_stalled_and_limit_ok():
    ticket = {
        'owner': 'nobody',
        'status': 'stalled',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 0,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_stalled_and_limit_over():
    ticket = {
        'owner': 'nobody',
        'status': 'stalled',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': False,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_stalled_and_no_limit():
    ticket = {
        'owner': 'nobody',
        'status': 'stalled',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {}

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_rejected_and_limit_ok():
    ticket = {
        'owner': 'nobody',
        'status': 'rejected',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 0,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_rejected_and_limit_over():
    ticket = {
        'owner': 'nobody',
        'status': 'rejected',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {
                'new': 7,
                'open': 1,
                'rejected': 7,
            }

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': False,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }

def test_create_ticket_possible_actions_user_vapi_status_rejected_and_no_limit():
    ticket = {
        'owner': 'nobody',
        'status': 'rejected',
    }
    email = 'vapi@uc.pt'
    config = DITICConfigMock()
    config.email_limits = {}

    number_tickets_per_status = {
        'new': 7,
        'open': 1,
    }

    create_ticket_possible_actions(config, ticket, email, number_tickets_per_status)
    assert ticket['kanban_actions'] == {
        'increase_priority': True,
        'decrease_priority': True,
        'back': True,
        'interrupted': False,
        'stalled': False,
        'forward': False,
    }
