#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
#
# This program aims in creating the structure for using with the web interface
#
from datetime import date
from datetime import timedelta
from time import time
from time import gmtime
from json import dump
from json import load

from ditic_kanban.rt_api_old import RTApi
from ditic_kanban.rt_api_old import get_list_of_tickets
from ditic_kanban.config import DITICConfig
from ditic_kanban.tools import group_result_by


def summary_filename(working_dir, filename):
    """
    This file returns the summary filename in the format of
        working_dir/YYYYMMDDHH-filename

    :param working_dir: pth to the file
    :param filename: the file name desired
    :return: a string with the path+date+"-"+filename
    """
    now = gmtime()
    return '%s/%04d%02d%02d%02d-%s' % (
        working_dir,
        now.tm_year,
        now.tm_mon,
        now.tm_mday,
        now.tm_hour,
        filename,
    )


def __generate_summary_file(rt_object, list_emails, list_status):
    """
    This function will search all tickets and generate a summary to be used by the summary report.

    :param rt_object: the rt_object for accessing get_list_of_tickets
    :param list_emails: A set with the known emails. It is a set to optimize the search
    :param list_status: A list of available status
    :return: summary (TODO: how it is done!)
    """
    # Get the date from which we start searching tickets.
    previous_date = (date.today() - timedelta(0)).isoformat()

    # First step: search for all tickets of known emails
    known_email_query = ''
    for email in DITICConfig().get_email_to_user().keys():
        if known_email_query:
            known_email_query += ' OR '
        known_email_query += ' Owner = "%s" ' % email
    email_query = ' AND ('+known_email_query+') '

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, r'Queue = "general" AND ( Resolved > "%s" '
                                                  r'OR ( Status != "deleted" ) ) %s' % (previous_date, email_query))
    except ValueError as e:
        raise ValueError('Error:' + str(e))

    # Second step: search for all tickets of DIR and DIR-INBOX
    try:
        response += get_list_of_tickets(rt_object, r'Queue = "general" AND ( "CF.{IS - Informatica e Sistemas}" = "DIR"'
                                                   r'OR "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" )'
                                                   r'AND Owner = "nobody"'
                                                   r'AND Status != "deleted" ')
    except ValueError as e:
        raise ValueError('Error:' + str(e))

    # Third step: search for all tickets of unknown emails
    known_email_query = ''
    for email in DITICConfig().get_email_to_user().keys():
        known_email_query += ' AND Owner != "%s" ' % email
    email_query = known_email_query+' AND Owner != "nobody" '

    # Get the information from the server.
    try:
        response += get_list_of_tickets(rt_object, '''
                                        Queue = "general" AND Status != "deleted"
                                        AND ( "CF.{IS - Informatica e Sistemas}" = "DIR"'
                                        OR "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" )
                                        %s
                                        ''' % email_query)
    except ValueError as e:
        if str(e) != 'no matching results.':
            raise ValueError('Error:' + str(e))

    # Lets create summary dictionary
    summary = dict()
    summary['unknown'] = {status: 0 for status in list_status}
    summary['dir'] = {status: 0 for status in list_status}
    summary['dir-inbox'] = {status: 0 for status in list_status}

    group_by_email = group_result_by(response, 'owner')
    for email in sorted(group_by_email.keys()):
        group_by_status = group_result_by(group_by_email[email], 'status')

        # If this email is known, then identify it
        # If user is nobody, then it can be DIR or DIR-INBOX
        # Otherwise, it is unknown!
        if email in list_emails:
            summary[email] = {status: 0 for status in list_status}
        elif email == 'nobody':
            pass
        else:
            email = 'unknown'

        # Count the number of tickets in every status for this email
        for status in sorted(group_by_status.keys()):
            if email == 'nobody':
                group_by_cf = group_result_by(group_by_status[status], 'cf.{is - informatica e sistemas}')
                summary['dir'][status] += len(group_by_cf.get('dir', ''))
                summary['dir-inbox'][status] += len(group_by_cf.get('dir-inbox', ''))
            else:
                summary[email][status] += len(group_by_status[status])
                #summary[email][status] =1337

    return summary


def generate_summary_file():
    """
    We need this function in order to test the real generate_summary_file function. Its name has been changed to __...

    :return: the time necessary to execute this function
    """
    start_time = time()

    # Read configuration
    config = DITICConfig()

    # List of emails
    list_emails = set(config.get_email_to_user().keys())

    # List of possible status
    list_status = config.get_list_status()

    # Let use system config list
    system = config.get_system()

    rt_object = RTApi(system['server'], system['username'], system['password'])

    summary = __generate_summary_file(rt_object, list_emails, list_status)

    # The summary of all files will be flushed to this file.
    try:
        with open(summary_filename(system['working_dir'], system['summary_file']), 'w') as file_handler:
            dump(summary, file_handler)
    except IOError as e:
        raise IOError('Error:' + str(e))

    return '%0.2f seconds' % (time() - start_time)


def get_summary_info():
    """
    returns a dictionary with the following format
        {
            'email':
                {
                    'status': 'value',
                    ...
                }
            ...
        }
    :return:
    """

    # Read configuration
    config = DITICConfig()

    # List of known emails
    list_emails = config.get_email_to_user().keys()

    # List of known status
    list_status = config.get_list_status()

    # Let use system config list
    system = config.get_system()

    # Get the file information
    try:
        with open(summary_filename(system['working_dir'], system['summary_file']), 'r') as file_handler:
            summary = load(file_handler)
    except IOError:
        # If there is an error, then return everything zeroed
        summary = {email: {status: 0 for status in list_status} for email in list_emails}
        summary['dir'] = {status: 0 for status in list_status}
        summary['dir-inbox'] = {status: 0 for status in list_status}
        summary['unknown'] = {status: 0 for status in list_status}

    return summary
