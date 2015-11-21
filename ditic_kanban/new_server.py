# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This module is responsible for web routing. This is the main web server.

import actions

from bottle import get
from bottle import post
from bottle import put
from bottle import template
from bottle import request
from bottle import run
from bottle import redirect
from bottle import route
from bottle import static_file


def start_server():
    run(server='paste', host='0.0.0.0', debug=True)
