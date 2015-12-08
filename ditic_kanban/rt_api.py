#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By LogicBox @2015
# This package will handle all communications with RT4 through python-RTkit
#

from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator


def login_user(server, username, password):
        """
        Attempts to login the provided user with RT4.
        Returns RTResource for further calls.

        :param server: server address
        :param username: username for authenticate
        :param password: password for authenticate
        :return: resource: RTResource for further calls or False if the login is invalid
        """
        resource = RTResource('http://'+server+'/REST/1.0/', username, password, CookieAuthenticator)
        response = resource.get(path='ticket/1')
        status_code = response.status_int

        if status_code == 401:
            return False

        return resource

def fetch_ticket_details(resource, ticket_id):
    response = resource.get(path='ticket/'+ticket_id)

