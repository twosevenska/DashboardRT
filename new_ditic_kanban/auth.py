#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This program will create an object that will manage users authentication
#
from random import randint

from ditic_kanban.config import DITICConfig
from ditic_kanban.rt_api import RTApi


class UserAuth:
    def __init__(self):
        self.config = DITICConfig()
        self.ids = {
            # Only used for tests...
            # u'10': {
            #     'email': 'olivio@uc.pt',
            #     'rt_object':  RTApi('server_address', 'username', 'password'),
            # }
        }

    def __get_new_id(self):
        while True:
            new_id = unicode(randint(0, 1000))
            if new_id not in self.ids:
                return new_id

    # noinspection PyTypeChecker
    def get_email_id(self, email):
        if email not in self.config.get_email_to_user().keys():
            raise ValueError('Unknown email')

        for uid in self.ids:
            if email == self.ids[uid]['email']:
                return uid

        raise ValueError('Unknown error! This should not be like this...')

    # noinspection PyTypeChecker
    def get_email_from_id(self, uid):
        if 'email' not in self.ids[uid]:
            raise ValueError('Unauthenticated user')
        return self.ids[uid]['email']

    # noinspection PyTypeChecker,PyTypeChecker
    def get_rt_object_from_email(self, email):
        if email not in self.config.get_email_to_user().keys():
            raise ValueError('Unknown email')

        for uid in self.ids:
            if email == self.ids[uid]['email']:
                return self.ids[uid]['rt_object']

        raise ValueError('Unknown error! This should not be like this...')

    def check_id(self, uid):
        """
        This function will check if id exists.
        It is important to say that id MUST be a unicode value!

        :param uid: unicode with id value
        :return: True or False, depending if ID exists or not
        """
        if uid in self.ids:
            return True
        return False

    def check_password(self, email, pwd):
        if email not in self.config.get_email_to_user().keys():
            raise ValueError('Unknown email')

        # Get system configurations
        system = self.config.get_system()

        # To check the password, we will try to check if user has any new ticket
        email_rt_api = RTApi(system['server'], email, pwd)

        data_dict = {'query': 'Owner = "%s" and Status = "new"' % email}
        response = email_rt_api.get_data_from_rest('/search/ticket', data_dict)
        if 'your username or password is incorrect' in response:
            raise ValueError('Password is incorrect')

        self.ids[self.__get_new_id()] = {
            'email': email,
            'rt_object': email_rt_api,
        }
        return True
