#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
from ditic_kanban.rt_summary import summary_filename
from ditic_kanban.rt_summary import __generate_summary_file

from mock_rt_api import RTApiMock


def test_summary_filename():
    result = summary_filename('/test_working_dir', 'test_filename')
    assert result.startswith('/test_working_dir')
    assert result.endswith('-test_filename')

def test_private__generate_summary_file():
    rt_object = RTApiMock()
    rt_object.set_return(
        [
            u'rt/4.0.6 200 ok', u'',
            u'id: ticket/887677',
            u'owner: vapi@uc.pt',
            u'status: open',
            u'cf.{is - informatica e sistemas}: dir-inbox',
            u'',
            u'rt/4.0.6 200 ok', u'',
            u'id: ticket/887677',
            u'owner: asantos@uc.pt',
            u'status: new',
            u'cf.{is - informatica e sistemas}: dir-inbox',
            u'',
        ]
    )
    list_emails = set(['vapi@uc.pt', 'asantos@uc.pt'])
    list_status = ['new', 'open']

    summary = __generate_summary_file(rt_object, list_emails, list_status)
    assert summary == {
        'unknown':
            {
                'new': 0,
                'open': 0,
            },
        u'asantos@uc.pt':
            {
                'new': 3,
                'open': 0,
            },
        'dir-inbox':
            {
                'new': 0,
                'open': 0,
            },
        u'vapi@uc.pt':
            {
                'new': 0,
                'open': 3,
            },
        'dir':
            {
                'new': 0,
                'open': 0
            }
    }


# As it is very complicated to mock the open function, I will pass those testes:
# generate_summary_file
# get_summary_info
#