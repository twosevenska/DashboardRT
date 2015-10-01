#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
from ditic_kanban.config import DITICConfig


def test_get_email_to_user():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.get_email_to_user()
    assert response == {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }

def test_get_system():
    test_config = DITICConfig()
    test_config.system = {
        'server': 'server_address',
        'username': 'username',
    }
    response = test_config.get_system()
    assert response == {
        'server': 'server_address',
        'username': 'username',
    }

def test_get_user_from_email():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.get_user_from_email('vapi@uc.pt')
    assert response == 'Vapi'

def test_get_email_from_user():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.get_email_from_user('Vapi')
    assert response == 'vapi@uc.pt'

def test_users_list():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.get_users_list()
    assert response == ['Vapi', 'Alex']

def test_get_email_limits():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    test_config.email_limits = {
        'vapi@uc.pt': {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }
    }
    response = test_config.get_email_limits('vapi@uc.pt')
    assert response == {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }

def test_get_email_limits_value():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    test_config.email_limits = {
        'vapi@uc.pt': {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }
    }
    response = test_config.get_email_limits('vapi@uc.pt', 'open')
    assert response == 1

def test_get_email_limits_unknown_email():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    test_config.email_limits = {
        'vapi@uc.pt': {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }
    }
    response = test_config.get_email_limits('unknown@uc.pt')
    assert response == {}

def test_get_email_limits_unknown_email_known_status():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    test_config.email_limits = {
        'vapi@uc.pt': {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }
    }
    response = test_config.get_email_limits('unknown@uc.pt', 'open')
    assert response == 0

def test_get_email_limits_known_email_unknown_status():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    test_config.email_limits = {
        'vapi@uc.pt': {
            'new': 7,
            'open': 1,
            'rejected': 7,
        }
    }
    response = test_config.get_email_limits('vapi@uc.pt', 'no_status')
    assert response == 0

def test_get_list_status():
    test_config = DITICConfig()
    test_config.list_status = [
            'new',
            'open',
    ]
    response = test_config.get_list_status()
    assert response == [
            'new',
            'open',
    ]

def test_check_if_user_exist_known_user():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.check_if_user_exist('Vapi')
    assert response == True

def test_check_if_user_exist_unknown_user():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.check_if_user_exist('Gina')
    assert response == False

def test_check_if_email_exist_known_email():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.check_if_email_exist('vapi@uc.pt')
    assert response == True

def test_check_if_email_exist_known_email():
    test_config = DITICConfig()
    test_config.email_to_user = {
        'vapi@uc.pt': 'Vapi',
        'asantos@uc.pt': 'Alex',
    }
    response = test_config.check_if_email_exist('gina.costa@uc.pt')
    assert response == False
