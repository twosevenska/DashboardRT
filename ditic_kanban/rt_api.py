#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By LogicBox @2015
# This package will handle all communications with RT4 through python-RTkit
#

from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator


def login_user(server, username, password):
    #TODO: Integration test
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
    #TODO: Integration test
    """
    Fetches the details of a particular ticket.

    :param resource: RTResource for the call
    :param ticket_id: Id of the ticket.
    :return: A non-null dictionary if the ticket exists, otherwise False
    """
    response = resource.get(path='ticket/'+ticket_id)

    if response.status_int == 404:
        return False

    ticket_details = dict(response.parsed[0])
    return ticket_details


def create_new_ticket(resource, new_values):
    #TODO: Integration test
    """
    Creates ticket.

    :param resource: RTResource for the call
    ::param new_values: a dictionary with a relation attribute and its new value. Example: { 'Status': 'new', ... }
    :return: Operation result
    """
    result = False
    content = {'content': new_values}
    response = resource.post(path='ticket/new', payload=content)

    if response.status_int == 200:
        result = True

    return result


def modify_ticket(resource, ticket_id, new_values):
    #TODO: Integration test
    """
    Modify ticket attributes. The first variable is the ticket ID to be changed. The second variable will be
    a dictionary with a combination of attribute and its new value

    :param ticket_id: the ticket ID (a string with the ticket number)
    :param new_values: a dictionary with a relation attribute and its new value. Example: { 'Status': 'new', ... }
    :return: Operation result
    """
    result = False
    content = {'content': new_values}

    response = resource.post(path='ticket/'+ticket_id, payload=content)

    if response.status_int == 200:
        result = True

    return result
