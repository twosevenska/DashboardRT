#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
from datetime import date
from datetime import timedelta
from datetime import datetime
from time import mktime
from time import strptime
from time import time
from time import gmtime
from json import load
from json import dump

from ditic_kanban.rt_api import RTApi
from ditic_kanban.rt_api import get_list_of_tickets
from ditic_kanban.config import DITICConfig


def stats_search_tickets(rt_object, query):
    """
    This function will get the list of tickets. As most tickets will have a specific criteria, we will use this
    function to include it by default.
    The criteria will be defined in the default_query variable.

    :param rt_object: RTApi object
    :param query: The string to be appended to the default_query variable
    :return: A number or a list, depending on the detail variable
    """
    if not query:
        raise ValueError('no query... error!')

    # The default query
    default_query = 'Queue = "General" AND '

    # The search query
    query = default_query+query

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query)
    except ValueError:
        return []

    return response


def stats_search_number_of_tickets(rt_object, query):
    """
    This function will get the number of tickets. As most tickets will have a specific criteria, we will use this
    function to include it by default.
    The criteria will be defined in the default_query variable.

    :param rt_object: RTApi object
    :param query: The string to be appended to the default_query variable
    :return: A number or a list, depending on the detail variable
    """
    if not query:
        raise ValueError('no query... error!')

    # The default query
    default_query = 'Queue = "General" AND ( "CF.{IS - Informatica e Sistemas}" = "DIR" ' \
                    'OR "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX" ) AND '

    # The search query
    query = default_query+query

    # Get the information from the server.
    try:
        response = get_list_of_tickets(rt_object, query, False)
    except ValueError as e:
        raise ValueError(str(e))

    return len(response)


def get_date(days, from_date=''):
    """
    Get the date in the format YYYY-MM-DD.
    If days == 0, return today's date.
    If day > 0, then return the date "days" before.

    :param days: number >= 0
    :param from_date: Date from which we start counting
    :return: string with date in format YYYY-MM-DD
    """
    if from_date:
        initial_date = datetime.strptime(from_date, '%Y-%m-%d')
    else:
        initial_date = date.today()
    return (initial_date - timedelta(days)).isoformat()[:10]


def number_of_created_tickets_on_a_date(rt_object, tickets_date):
    """
    Return the number of tickets created on a specific date.

    :param rt_object: RTApi object
    :param tickets_date: date in format YYY-MM-DD
    :return: the number of tickets found
    """
    # Get the information from the server.
    try:
        response = stats_search_number_of_tickets(rt_object, 'Created ="%s"' % tickets_date)
    except ValueError:
        return 0

    return response


# noinspection PyArgumentList
def stats_mean_time(start_date, final_date):
    """
    Return the number of minutes that the ticket took from created time and resolve time.

    :param start_date: start date (YYYY-MM-DD)
    :param final_date: end date (YYYY-MM-DD)
    :return: integer number of minutes to solve the ticket
    """
    # noinspection PyArgumentList
    result = mktime(strptime(final_date)) - mktime(strptime(start_date))
    result /= 60

    # If results are higher than 1 month of work, then forget it!
    # ( 60 minutes * 24 hours a day * 30 days = 43 200 minutes)
    if result > 43200:
        return 0
    else:
        return result


def stats_number_of_tickets_of_an_user(list_tickets, email):
    """
    Return a dictionary of all possible status and the number of tickets in each status.

    :param list_tickets: list of all tickets to be analyzed
    :param email: a string with the email of the user
    :return: a dictionary with the number of tickets per status
    """
    # Initialize the result
    result = {
        'resolved': 0,
        'open': 0,
        'time_worked': 0,
        'number_of_urgent_tickets': 0,
        'number_of_interrupted_times': 0,
    }

    # Analise the response and place the correct number in the status
    time_to_resolve = []
    for line in list_tickets:
        if email and line['owner'] != email:
            continue

        if line['status'] == 'resolved':
            time_to_resolve.append(stats_mean_time(line['created'], line['resolved']))
            result['resolved'] += 1

            # Does we have the time worked?
            if 'timeworked' in line:
                if 'minutes' in line['timeworked']:
                    result['time_worked'] += int(line['timeworked'][:line['timeworked'].find(' minutes')])
                elif line['timeworked'] == '0':
                    pass
                else:
                    raise ValueError('Not minutes:'+str(line['timeworked']))

            # Has this ticket been marked as urgent?
            if 'cf.{ditic-urgent}' in line and line['cf.{ditic-urgent}'] == 'yes':
                result['number_of_urgent_tickets'] += 1

            # Has this ticket been interrupted?
            if 'cf.{ditic-interrupted}' in line and line['cf.{ditic-interrupted}']:
                result['number_of_interrupted_times'] += int(line['cf.{ditic-interrupted}'])

        elif line['status'] == 'deleted':
            # Ignore deleted tickets!
            pass
        else:
            result['open'] += 1

    if time_to_resolve:
        result['mean_time_to_resolve'] = sum(time_to_resolve)/len(time_to_resolve)
    else:
        result['mean_time_to_resolve'] = 0

    return result


def full_list_of_tickets_on_a_date(rt_object, config, tickets_date):
    """
    Search information of all created tickets, all tickets that has been modified in the specified date.
    The result will be the following:
        {
            'create_tickets': # of created tickets,
            'team': {
                'status 1': # of tickets on that state,
                ...
            }
            'team_members': {
                'email1': {
                    'status1': # tickets,
                    ...
                }
            }
        }

    The search criteria is very complex. It has to be so because we need to satisfy the following:
    - All tickets in the DIR or DIR-INBOX that has been closed this day or are still not resolved nor deleted
    - All tickets of all known users that has been closed this day or are still not resolved nor deleted

    :param rt_object: RTApi object
    :param config: DITICConfig object
    :param tickets_date: the date for searching in format YYYY-MM-DD
    :return: a dictionary
    """
    emails = config.email_to_user.keys()

    result = {'created_tickets': number_of_created_tickets_on_a_date(rt_object, tickets_date)}

    query = '''
            (("CF.{IS - Informatica e Sistemas}" = "DIR" OR "CF.{IS - Informatica e Sistemas}" = "DIR-INBOX")
             AND Owner = "nobody"
             AND (LastUpdated = "%s" OR Status = "new" OR Status = "open" OR Status = "stalled" OR Status = "rejected"))
    ''' % tickets_date
    list_of_tickets = stats_search_tickets(rt_object, query)

    for email in emails:
        query = '''
                ( owner = "%s"
                AND (LastUpdated = "%s" OR Status = "new"
                     OR Status = "open" OR Status = "stalled"
                     OR Status = "rejected"))
        ''' % (email, tickets_date)
        list_of_tickets += stats_search_tickets(rt_object, query)

    result['team'] = stats_number_of_tickets_of_an_user(list_of_tickets, '')
    result['team_members'] = {}
    for email in emails:
        result['team_members'].update(
            {
                email: stats_number_of_tickets_of_an_user(list_of_tickets, email)
            }
        )

    return result


def generate_filename(working_dir, filename):
    """
    This file returns the summary filename in the format of
        working_dir/YYYYMMDDHH-filename

    :param working_dir: pth to the file
    :param filename: the file name desired
    :return: a string with the path+date+"-"+filename
    """
    now = gmtime()
    return '%s/%04d%02d-%s' % (
        working_dir,
        now.tm_year,
        now.tm_mon,
        filename,
    )


def read_statistics_file(config):
    """
    Read from the specified JSON file.

    :param config: DITICConfig object
    :return: a dictionary
    """
    system = config.get_system()

    # Get the file information
    try:
        with open(generate_filename(system['working_dir'], system['statistics_file']), 'r') as file_handler:
            return load(file_handler)
    except IOError:
        return {}
    except ValueError:
        return {}


def write_statistics_file(config, result, desired_year, desired_month):
    system = config.get_system()

    filename = '%s/%s%s-%s' % (system['working_dir'],
                               desired_year,
                               desired_month,
                               system['statistics_file'])

    # Get the file information
    try:
        with open(filename, 'w') as file_handler:
            dump(result, file_handler)
    except IOError as e:
        raise IOError('Error:' + str(e))


def stats_update_json_file(number_of_days=1):
    """
    Reads old json file, if it exists, get new information, update statistics, write back to file
    There is a known bug: the number_of_days MUST not overlap a month If it does, there will be a problem ;)

    :param number_of_days: Number of days to analyze
    :return: time took to execute
    """
    # TODO: guarantee that the data is written in the correct filename, if number_of_days overlap a month
    start_time = time()

    config = DITICConfig()
    system = config.get_system()
    rt_object = RTApi(system['server'], system['username'], system['password'])

    # result = read_statistics_file(config)
    for this_day in range(0, number_of_days):
        current_date = get_date(this_day)
        current_year_month = current_date[:7]
        result = stats_read_json_file(current_year_month[:4], current_year_month[5:7])
        result[get_date(this_day)] = full_list_of_tickets_on_a_date(rt_object, config, current_date)
        write_statistics_file(config, result, current_year_month[:4], current_year_month[5:7])

    return '%0.2f seconds' % (time() - start_time)


def stats_read_json_file(desired_year, desired_month):
    """
    Just read the JSON file for the request year and month.
    It will return everything on this file.

    :param desired_month:
    :return:
    """
    system = DITICConfig().get_system()
    filename = '%s/%s%s-%s' % (system['working_dir'],
                               desired_year,
                               desired_month,
                               system['statistics_file'])

    # Get the file information
    try:
        with open(filename, 'r') as file_handler:
            return load(file_handler)
    except IOError:
        return {}
    except ValueError:
        return {}


def get_statistics(start_date, end_date):
    """
    The goal here is to return all statistics information we have between those days.
    The date format MUST be in YYYY-MM-DD

    :param start_date: string with first day in YYYY-MM-DD
    :param end_date: string with last day in YYYY-MM-DD
    :return: a dictionary with the statistics
    """
    result_dates = {}
    current_date = end_date
    month_data = {}
    count_days = 0

    # We get all desired days
    while current_date > start_date:
        current_year_month = current_date[:7]

        # If we don't have data, get it...
        if current_year_month not in month_data:
            month_data[current_year_month] = stats_read_json_file(current_year_month[:4], current_year_month[5:7])

        # Add the desired info, if it exists...
        if current_date in month_data[current_year_month]:
            result_dates[current_date] = month_data[current_year_month][current_date]
        else:
            result_dates[current_date] = {}

        count_days += 1
        current_date = get_date(count_days, end_date)

    return result_dates
