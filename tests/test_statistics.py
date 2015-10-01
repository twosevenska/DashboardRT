#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
import pytest

from ditic_kanban.statistics import stats_search_tickets
from ditic_kanban.statistics import stats_search_number_of_tickets
from ditic_kanban.statistics import number_of_created_tickets_on_a_date
from ditic_kanban.statistics import stats_number_of_tickets_of_an_user

from mock_rt_api import RTApiMock

def test_stats_search_tickets_query_ok():
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
    response = stats_search_tickets(rt_object, 'My search')
    assert response == [
        {
            u'status': u'open',
            u'priority': u'26',
            u'lastupdated': u'wed jul 15 21:16:50 2015',
            u'owner': u'vapi@uc.pt',
            u'cf.{is - informatica e sistemas}': u'dir-inbox',
            'id': u'887677',
            u'cf.{servico}': u'csc-gsiic',
            u'subject': u'create rt dashboard'
        }
    ]


def test_stats_search_tickets_query_not_ok():
    rt_object = RTApiMock()
    rt_object.set_return(['no matching results.'])
    result = stats_search_tickets(rt_object, 'My search')
    assert result == []


def test_stats_search_number_of_tickets_query_ok():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'812344: create rt dashboard',
    ])
    response = stats_search_number_of_tickets(rt_object, 'My search')
    assert response == 1


def test_stats_search_number_of_tickets_query_not_ok():
    rt_object = RTApiMock()
    rt_object.set_return(['no matching results.'])
    with pytest.raises(ValueError) as value_error:
        stats_search_number_of_tickets(rt_object, 'My search')
    assert 'no matching results.' in str(value_error)


def test_number_of_created_tickets_on_a_date_query_ok():
    rt_object = RTApiMock()
    rt_object.set_return([
                u'812344: create rt dashboard',
    ])
    response = number_of_created_tickets_on_a_date(rt_object, 'My search')
    assert response == 1


def test_number_of_created_tickets_on_a_date_query_not_ok():
    rt_object = RTApiMock()
    rt_object.set_return(['no matching results.'])
    response = number_of_created_tickets_on_a_date(rt_object, 'My search')
    assert response == 0


def test_stats_number_of_tickets_of_an_user_query_ok():
    list_of_tickets = [
        {
            'owner': 'vapi@uc.pt',
            'status': 'resolved',
            'created': 'wed jul 15 21:16:50 2015',
            'resolved': 'wed jul 15 23:16:00 2015',
            'cf.{ditic-interrupted}': '5',
            'cf.{ditic-urgent}': 'yes',
        }
    ]
    response = stats_number_of_tickets_of_an_user(list_of_tickets, 'vapi@uc.pt')
    assert response == {
        'resolved': 1,
        'mean_time_to_resolve': 119.16666666666667,
        'open': 0,
        'time_worked': 0,
        'number_of_interrupted_times': 5,
        'number_of_urgent_tickets': 1,
    }


def test_stats_number_of_tickets_of_an_user_query_no_mean_time_to_resolve():
    list_of_tickets = [
        {
            'owner': 'vapi@uc.pt',
            'status': 'open',
            'created': 'wed jul 15 21:16:50 2015',
            'resolved': 'not set',
        }
    ]
    response = stats_number_of_tickets_of_an_user(list_of_tickets, 'vapi@uc.pt')
    assert response == {
        'resolved': 0,
        'mean_time_to_resolve': 0,
        'open': 1,
        'time_worked': 0,
        'number_of_interrupted_times': 0,
        'number_of_urgent_tickets': 0,
    }
