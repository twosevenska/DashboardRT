#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Logic Box @2015
# This file contains several functions that do several operations necessary to this package to work
#
from bottle import put

@put('/action/forward/<ticket_id:int>')
def on_action_forward(ticket_id):
	print("forward:"+str(ticket_id))
	