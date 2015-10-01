#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# RTApi test mock
#


class RTApiMock:
    """Mock of the RTApi"""
    def __init__(self, *args, **kargs):
        self.return_value = ''
        self.uri = ''
        self.data = ''
        pass

    def set_return(self, return_value):
        self.return_value = return_value

    def get_data_from_rest(self, uri, data):
        self.uri = uri
        self.data = data
        return self.return_value
