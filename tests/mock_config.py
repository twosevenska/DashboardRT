#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# RTApi test mock
#


class DITICConfigMock:
    def __init__(self):
        self.email_to_user = {
            'vapi@uc.pt': 'Vapi',
            'asantos@uc.pt': 'Alex',
        }
        self.email_limits = {
            'vapi@uc.pt': {
                'new': 7,
                'open': 1,
                'rejected': 7,
            },
            'asantos@uc.pt': {
                'new': 14,
                'open': 2,
                'rejected': 14,
            },
        }
        self.list_status = [
            'new',
            'open',
        ]
        self.system = {
            'working_dir': '/usr/local/dir/tmp/ditic-rt',
            'summary_file': 'summary',
            'server': 'server_address',
            'username': 'username',
            'password': 'password',
        }


    def get_email_limits(self, *args, **kargs):
        return self.email_limits

