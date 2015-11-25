#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This package will create an interface with RT4, using its REST API
#
import cookielib
import urllib
import urllib2
from re import findall


class RTApi:
    """Class for contacting RT server through REST API"""

    def __init__(self, server, username, password):
        """
        Creates local variables, create a cookie for connecting with server.
        All communication with RT will be like HTTP/1.0 (connect, authenticate,
        get information, disconnect. A new connection will imply restart everything)

        :param server: server address
        :param username: username for authenticate
        :param password: password for authenticate
        :return: Null
        """
        self.server = server
        self.username = username
        self.password = password

        # Creates cookies for REST
        self.cookielib = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookielib))

        return

    def get_data_from_rest(self, uri, data):
        """
        This function will contact the REST server and will return the result in the form of a list.
        Each element of the list is a line striped (enters removed)
        I'm not quite sure about it, but by now I'm applying "".decode('utf-8') due to portuguese characters.

        :param uri: string with the value to be added to https://server/REST/1.0/
            see this URL for options: http://requesttracker.wikia.com/wiki/REST
        :param data: dictionary with parameters to be added to the list with user and pwd
        :return: list with the result of the query
                 will return and empty list if no result obtained
        """
        # Use the correct cookie
        urllib2.install_opener(self.opener)

        uri = 'http://' + self.server + '/REST/1.0/' + uri
        data = data or dict()
        data.update({'user': self.username, 'pass': self.password})
        data_url_encode = urllib.urlencode(data)
        login = urllib2.Request(uri, data_url_encode)

        try:
            response = urllib2.urlopen(login)
            return [i.decode('utf-8').strip().lower() for i in response]
        except urllib2.URLError:
            # Could not contact server!
            raise ValueError('Not able to contact server!')


def get_list_of_tickets(rt_object, query, detail=True):
    """
    Get a full list of all tickets, and its information, based on the query.

    The query should be a string with the RT4 syntax for querying the DB
    Example of query could be:
        '(Owner="vapi@uc.pt" OR Owner="asantos@uc.pt") AND Status != "Resolved" AND Status != "Rejected"'

    The result of this query will be a list with the following format:
        [
            [ <ticketID>,
                {
                    <field>: <value>,
                    ...
                }
            ],
            ...
        ]

    The param detail will define if we want detailed information in the response. By default is yes

    :param query: a string with the query
    :param detail: a boolean. True if we want detailed answer (default). False otherwise.
    :return: a list
    """
    data_dict = {'query': query}
    if detail:
        data_dict.update({'format': 'l'})
    response = rt_object.get_data_from_rest('/search/ticket', data_dict)
    result = []
    # In this section, we must transform the result from server into the format
    # this function is supposed to return
    for line in response:

        # If the result is an error, return without any response (raise an exception)
        if line.startswith('your username or password is incorrect') \
                or line.startswith('invalid query:') \
                or line.startswith('no matching results.'):
            raise ValueError(line)

        # Ignore those lines...
        if line.startswith('rt/4') or line == '' or line == '--':
            continue

        # Here, we get the ticket ID. This information is critical
        if line.startswith('id: ticket/'):
            result.append({'id': line[11:]})
            continue

        # If we get into this part, then we must get the pair key / value returned by server
        find_semicolon = line.find(':')
        find_previous = line[:find_semicolon]
        find_after = line[find_semicolon + 2:]

        # Populate the result variable
        if detail:
            result[-1].update({find_previous: find_after})
        else:
            result.append(
                {
                    'id': find_previous,
                    'subject': find_after,
                }
            )

    return result


def get_list_of_users(rt_object, detail=True):
    """
    Get a full list of all tickets, and its information, based on the query.

    The query should be a string with the RT4 syntax for querying the DB
    Example of query could be:
        '(Owner="vapi@uc.pt" OR Owner="asantos@uc.pt") AND Status != "Resolved" AND Status != "Rejected"'

    The result of this query will be a list with the following format:
        [
            [ <ticketID>,
                {
                    <field>: <value>,
                    ...
                }
            ],
            ...
        ]

    The param detail will define if we want detailed information in the response. By default is yes

    :param query: a string with the query
    :param detail: a boolean. True if we want detailed answer (default). False otherwise.
    :return: a list
    """

    response = rt_object.get_data_from_rest('/user/')

    return response


def modify_ticket(rt_object, ticket_id, new_values):
    """
    Modify ticket attributes. The first variable is the ticket ID to be changed. The second variable will be
    a dictionary with a combination of attribute and its new value

    :param ticket_id: the ticket ID (a string with the ticket number)
    :param new_values: a dictionary with a relation attribute and its new value. Example: { 'Status': 'new', ... }
    :return: Operation result
    """
    content = ''
    for key in new_values:
        content += key + ': ' + new_values[key] + '\n'

    # Information required for RT query
    uri = 'ticket/' + str(ticket_id) + '/edit'
    data = {'content': content}

    # Modify the ticket
    try:
        return rt_object.get_data_from_rest(uri, data)
    except ValueError as e:
        raise ValueError(e)


def create_new_ticket(rt_object, new_values):
    """
    Creates ticket.The first variable will be a dictionary with
    a combination of new attributes.

    ::param new_values: a dictionary with a relation attribute and its new value. Example: { 'Status': 'new', ... }
    :return: Operation result
    """
    content = ''
    for key in new_values:
        content += key + ': ' + new_values[key] + '\n'

    # Information required for RT query
    uri = 'ticket/new'
    data = {'content': content}

    # Create the ticket
    try:
        return rt_object.get_data_from_rest(uri, data)
    except ValueError as e:
        raise ValueError(e)


def get_ticket_links(rt_object, ticket_id):
    """
    Get the list of links of a ticket_id.
    The result will be a list in the format:
        [
            ['attribute', 'value']
            ...
        ]

    Possible attributes:
    - members (children), memberof (parents)
    -

    :param rt_object: the RTApi object
    :param ticket_id: the ticket ID
    :return: a list with a line and
    """
    response = rt_object.get_data_from_rest('/ticket/%s/links/show' % ticket_id, {})

    result = []
    old_item = ''
    for line in response:
        search_item = findall(r'^([^:]+): .*/(\d+)(,)?$', line)
        if search_item:
            result.append([search_item[0][0], search_item[0][1]])
            old_item = search_item[0][0]
            continue

        # Does it is a multiple line response?
        search_item = findall(r'^fsck.com-rt:.*/(\d+)(,)?$', line)
        if search_item:
            result.append([old_item, search_item[0][0]])
            continue

    return result

def fetch_ticket_details(rt_object, ticket_id):
    """
    Fetches the details of a particular ticket.

    :param rt_object: a non-null RTApi.
    :param ticket_id: an integer.
    :return: A non-null dictionary.
    """

    response = rt_object.get_data_from_rest('/ticket/{id}'.format(id=ticket_id), {})

    result = {} # We start with an empty dictionary.

    # The response's body should contain several lines with the format
    # <attribute>:<value>. We add a pair to the resulting dictionary as we find them.
    for line in response :
        attribute = _extract_attribute(line)
        value = _extract_value(line)
        if attribute is not None and value is not None:
            result.update({attribute: value})

    return result


def fetch_ticket_brief_history(rt_object, ticket_id):
    """
    Fetches the history, with a brief format, of a particular ticket.

    :param rt_object: a non-null RTApi.
    :param ticket_id: an integer.
    :return: A non-null dictionary.
    """

    response = rt_object.get_data_from_rest('/ticket/{id}/history'.format(id=ticket_id), {})

    result = [] # We start with an empty dictionary.

    # The response's body should contain several lines with the format
    # <attribute>:<value>. We add a pair to the resulting dictionary as we find them.
    for line in response :
        attribute = _extract_attribute(line)
        value = _extract_value(line)
        if attribute is not None and value is not None:
            result.append((int(attribute), value))

    return sorted(result, reverse=True)


def _extract_attribute(line):
    """
    Given a string with the format <attribute>:<value>, this function extracts
    the <attribute> and strips it from spaces.

    For example, given the string '  foo: bar  ', this function return 'foo'.

    If the string does not contain a colon, then None is returned.

    :param line: a non-null string
    :return: a string, or None
    """

    try:
        return line[ : line.index(':')].strip()
    except ValueError, e:
        return None

def _extract_value(line):
    """
    Given a string with the format <attribute>:<value>, this function extracts
    the <value> and strips it from spaces.

    For example, given the string '  foo: bar  ', this function return 'bar'.

    If the string does not contain a colon, then None is returned.

    :param line: a non-null string
    :return: a string, or None
    """

    try:
        return line[(line.index(':') + 1) : ].strip()
    except ValueError, e:
        return None

