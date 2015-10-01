#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# Tests for the rt_api class and functions
#
import pytest

from ditic_kanban.rt_api import get_list_of_tickets
from ditic_kanban.rt_api import modify_ticket
from ditic_kanban.rt_api import get_ticket_links

from mock_rt_api import RTApiMock

def test_get_list_of_tickets_ok():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'rt/4.0.6 200 ok', u'',
                u'id: ticket/887677',
                u'queue: general',
                u'owner: vapi@uc.pt',
                u'creator: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'initialpriority: 25',
                u'finalpriority: 75',
                u'requestors: vapi@uc.pt',
                u'cc:',
                u'admincc:',
                u'created: wed jul 15 21:17:29 2015',
                u'starts: fri jul 24 13:08:34 2015',
                u'started: wed jul 15 21:17:38 2015',
                u'due: not set',
                u'resolved: sun jul 19 02:29:03 2015',
                u'told: not set',
                u'lastupdated: fri jul 24 13:08:14 2015',
                u'timeestimated: 0',
                u'timeworked: 1026 minutes',
                u'timeleft: 0',
                u'cf.{servico}: csc-gsiic',
                u'cf.{n\xba de equipamento}:',
                u'cf.{tipo interven\xe7\xe3o}:',
                u'cf.{is - informatica e sistemas}: dir-inbox',
                u'cf.{sistema}:',
                u'cf.{estado gsiic}:',
                u'cf.{prioridade do requerente}:',
                u'cf.{notas}:',
                u'cf.{tipo de pedido}:',
                u'cf.{linkreport}: relatorio'
            ]
    )

    # Test if everything is ok...
    result = get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"')

    assert result == [
        {
            u'status': u'open',
            u'resolved': u'sun jul 19 02:29:03 2015',
            u'cf.{n\xba de equipamento}': u'',
            u'creator': u'vapi@uc.pt',
            u'cc': u'',
            u'started': u'wed jul 15 21:17:38 2015',
            u'requestors': u'vapi@uc.pt',
            u'cf.{servico}': u'csc-gsiic',
            u'owner': u'vapi@uc.pt',
            u'cf.{is - informatica e sistemas}': u'dir-inbox',
            'id': u'887677',
            u'subject': u'create rt dashboard',
            u'queue': u'general',
            u'cf.{sistema}': u'',
            u'timeleft': u'0',
            u'cf.{tipo de pedido}': u'',
            u'cf.{prioridade do requerente}': u'',
            u'created': u'wed jul 15 21:17:29 2015',
            u'cf.{notas}': u'',
            u'starts': u'fri jul 24 13:08:34 2015',
            u'due': u'not set',
            u'lastupdated': u'fri jul 24 13:08:14 2015',
            u'timeworked': u'1026 minutes',
            u'priority': u'26',
            u'admincc': u'', u'cf.{tipo interven\xe7\xe3o}': u'',
            u'cf.{estado gsiic}': u'', u'timeestimated': u'0',
            u'initialpriority': u'25', u'finalpriority': u'75',
            u'cf.{linkreport}': u'relatorio',
            u'told': u'not set'
        }
    ]

def test_get_list_of_tickets_invalid_username_or_password():
    rt_object = RTApiMock()
    rt_object.set_return(['your username or password is incorrect'])
    with pytest.raises(ValueError) as value_error:
        get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"')
    assert 'your username or password is incorrect' in str(value_error)

def test_get_list_of_tickets_invalid_query():
    rt_object = RTApiMock()
    rt_object.set_return(['invalid query:'])
    with pytest.raises(ValueError) as value_error:
        get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"')
    assert 'invalid query' in str(value_error)

def test_get_list_of_tickets_no_results():
    rt_object = RTApiMock()
    rt_object.set_return(['no matching results.'])
    with pytest.raises(ValueError) as value_error:
        get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"')
    assert 'no matching results.' in str(value_error)

def test_get_list_of_tickets_detail_True():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
                u'rt/4.0.6 200 ok', u'',
                u'id: ticket/887677',
                u'owner: vapi@uc.pt',
                u'subject: create rt dashboard',
                u'status: open',
                u'priority: 26',
                u'cf.{servico}: csc-gsiic',
                u'cf.{is - informatica e sistemas}: dir-inbox',
            ]
    )
    result = get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"', True)
    assert rt_object.uri == '/search/ticket'
    assert rt_object.data == {
        'query': 'Owner = "vapi@uc.pt" and Status == "open"',
        'format': 'l'
    }
    assert result == [
        {
            u'status': u'open',
            u'priority': u'26',
            u'owner': u'vapi@uc.pt',
            u'cf.{is - informatica e sistemas}': u'dir-inbox',
            u'id': u'887677',
            u'cf.{servico}': u'csc-gsiic',
            u'subject': u'create rt dashboard'
        }
    ]

def test_get_list_of_tickets_detail_False():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
            u'rt/4.0.6 200 ok', u'',
            u'887677: create rt dashboard',
        ]
    )
    result = get_list_of_tickets(rt_object, 'Owner = "vapi@uc.pt" and Status == "open"', False)
    assert rt_object.uri == '/search/ticket'
    assert rt_object.data == {
        'query': 'Owner = "vapi@uc.pt" and Status == "open"',
    }
    assert result == [
        {
            u'subject': u'create rt dashboard',
            u'id': u'887677',
        }
    ]

def test_modify_ticket():
    rt_object = RTApiMock()
    rt_object.set_return([u'rt/4.0.6 200 ok', u'', u'# ticket 887677 updated.', u''])
    result = modify_ticket(rt_object, '881188', {'Owner': 'vapi@uc.pt'})
    assert result == [u'rt/4.0.6 200 ok', u'', u'# ticket 887677 updated.', u'']

def test_get_ticket_links():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
            u'rt/4.0.6 200 ok',
            u'',
            u'id: ticket/885775/links',
            u'',
            u'members: fsck.com-rt://uc.pt/ticket/887677,',
            u'fsck.com-rt://uc.pt/ticket/897183,',
            u'fsck.com-rt://uc.pt/ticket/899145',
            u'',
            u''
        ]
    )
    result = get_ticket_links(rt_object, 885775)
    assert result == [[u'members', u'887677'], [u'members', u'897183'], [u'members', u'899145']]
