#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
# TODO: class manage project object
# TODO      - Create tree based on one ticket ID
# TODO      - Return tree starting on a ticket ID
# TODO      - store all known projects
# TODO      - save a set with all tickets ID related with root ticket ID
# TODO          use a set in order to get a search cost of O(lg n)
# TODO      - fast insert (create tree based on JSON file information)
# TODO
# TODO: function create known projects
# TODO      - Generate known projects
# TODO      - Create JSON file
# TODO
# TODO: function to read tree
# TODO      - Read from JSON file
# TODO
from time import ctime
from time import time

from ditic_kanban.rt_api import get_ticket_links
from ditic_kanban.rt_api import get_list_of_tickets


class ProjectObject:
    """
    This class will contain a single element object. All this element objects will contains the following information:
    - A n-ary list with the real structure of the tree. This list will contain:
        - a list with all ProjectObject children pointers
        - a pointer to the parent
    """

    def __init__(self, element, ticket_list, update_time, time_worked, time_estimated, time_left):
        """
        Create the element object. It will need the following information:
        - the element and it's subject
        - The date/time of it's last update
        - time worked so far
        - Estimated time for overall element (ticket) work
        - Time left to conclude the element work

        We will, also, create the following information:
        - Project time worked. This value is calculated that way:
            Element_project_time_worked = Element_time_worked + Element_child_1_project_time_worked + ...
            This information will be generated in a "Merkle tree" way
        - Project time estimated (the same way as the previous)
        - Project time left (the same way as the previous)
        As, at the beginning the element don't have children, then place in the project information the same
        information as the element times.

        :param element: integer with the ticket ID
        :param ticket_list: ticket list with all ticket information
        :param update_time: Time when this object was created (updating project date won't affect this)
        :param time_worked: integer with the time worked
        :param time_estimated: integer with the time estimated to execute the work
        :param time_left: integer with the time left to conclude the work
        :return: Null
        """
        # Basic checks
        if not (isinstance(element, int)
                and isinstance(time_worked, int)
                and isinstance(time_estimated, int)
                and isinstance(time_left, int)):
            raise ValueError('value error: Expecting integers!')

        # The element information
        self.element = element
        self.ticket_list = ticket_list
        self.update_time = update_time
        self.element_time_worked = time_worked
        self.element_time_estimated = time_estimated
        self.element_time_left = time_left

        # Project information
        self.project_time_worked = time_worked
        self.project_time_estimated = time_estimated
        self.project_time_left = time_left

        # BST information
        self.bst_left = ''
        self.bst_right = ''

        # n-ary list
        self.parent = ''
        self.children = []

        return

    def add_list_child(self, project_object):
        """
        Add the children to the list and update the project times

        :param project_object: the element ProjectObject object
        :return: Null
        """
        self.children.append(project_object)
        project_object.parent = self
        project_object.update_project_times()

        return

    def update_project_times(self):
        """
        Update the project times, and force parents to also update info.

        :return: Null
        """
        # Update my project times
        self.project_time_worked = self.element_time_worked
        self.project_time_estimated = self.element_time_estimated
        self.project_time_left = self.element_time_left
        for element in self.children:
            self.project_time_worked += element.project_time_worked
            self.project_time_estimated += element.project_time_estimated
            self.project_time_left += element.project_time_left

        # Request parent's update of project times (Merkle tree)
        if self.parent:
            self.parent.update_project_times()

        return

    def elements_children_list(self):
        """
        Returns the element children list.
        This will cycle every child and generate a list with the result.
        The output format will be:
            [
                element (ticket ID),
                project_time_worked,
                project_time_estimated,
                project_time_left,
                [
                    list of child 1
                    ...
                ]
            ]

        :return: A list with the previous format
        """
        return [
            self.element,
            self.ticket_list,
            self.project_time_worked,
            self.project_time_estimated,
            self.project_time_left,
            [child.elements_children_list() for child in self.children]
        ]

    def delete_object(self):
        """
        This single method will remove this object and all its children.

        :return: a list with all elements (ticket id) deleted
        """
        result = [self.element]

        # Remove all pointers
        for i in range(len(self.children)):
            child = self.children.pop()
            result += child.delete_object()
        if self.parent:
            self.parent.remove_child(self.element)
            self.parent = ''

        return result

    def remove_child(self, element):
        for child in self.children:
            if child.element == element:
                self.children.remove(child)
        return


class ProjectElementFastSearch:
    """
    Initially, a binary search tree (BST) solution for finding a ticket ID was planned. However, as tickets are created
    on a regular basis, from a lower number to a upper number, there is a great probability of getting a cost of O(n)
    for the BST. When updating the information we would get a cost of O(n^2).
    That way, a switch to ordered lists was the winner. With this solution we will get:
    - O(lg n) for searching an element
    - O(1) for adding an element, with a O(lg n) for the first ordering - only done with a search for an unordered list
    - O(n lg n) for updating

    The list of elements will be populated that way:
        [
            [
                'ticket_id',
                'ticket_id_ProjectObject_pointer',
            ]
            ...
        ]
    """
    def __init__(self):
        self.list = []
        self.is_ordered = False

        # Those variables are necessary for the O(lg n) search
        self.min = 0
        self.mean = 0
        self.max = 0

        return

    def insert_element(self, element, pointer):
        """
        Receive the element and pointer and insert it into the list.
        Cost: O(1)

        :param element: a number with the ticket id
        :param pointer: the ProjectObject pointer
        :return: null
        """
        if not isinstance(element, int):
            raise ValueError('value error: Expecting integers!')
        self.list.append([element, pointer])
        self.is_ordered = False

        return

    def remove_element(self, element):
        """
        The goal here is to remove one element from the list.
        The cost of this operation will be O(lg n * lg n), assuming that list.remove() will cost O(lg n)

        :param element: the ticket id
        :return: Null
        """
        if not isinstance(element, int):
            raise ValueError('value error: Expecting integers!')

        element = self.search_list(element)
        if element:
            self.list.remove(element)
            self.is_ordered = False

        return

    def order_list(self):
        """
        Sort the list

        :return:
        """
        if not self.is_ordered:
            self.list = sorted(self.list)
            self.is_ordered = True

        return

    def search_list(self, element):
        """
        Return the element and pointer.
        If not found return an empty list

        :param element: the element to search
        :return: a list with the result
        """
        # If the list is empty, return a null list
        if not self.list:
            return []

        # Sort the list, if it is unsorted
        self.order_list()

        # Search the sorted list
        self.min = 0
        self.max = len(self.list)
        self.mean = (self.min + self.max)/2

        # Cycle searching for the element
        while self.mean >= 0:
            # Three possible options:
            # - Value found (return it)
            # - Value is lesser than mean (deep search)
            # - Value is bigger than mean (deep search)
            if element == self.list[self.mean][0]:
                return self.list[self.mean]
            elif element < self.list[self.mean][0]:
                self.max = self.mean
            else:
                self.min = self.mean

            # Create new mean and search for the element
            old_mean = self.mean
            self.mean = (self.min + self.max)/2

            # If the mean value didn't change, then we didn't find the element!
            if old_mean == self.mean:
                break

        # We didn't found it...
        return []


class ManageProjectElements:
    """
    This class will manage projects, the relations between elements, recreate trees and all basic operations
    """
    def __init__(self):
        self.project_class = ProjectObject
        self.elements = ProjectElementFastSearch()

        return

    def add_element(self, element, parent, element_dict):
        """
        Insert an element (ticket ID).
        If a parent is added, then try to insert it into the correct place.

        :param element: an integer with the element
        :param parent: an integer with the parent element
        :param element_dict: the ticket dictionary
        :return: null
        """
        # Element and parent must be integers
        if not isinstance(element, int):
            raise ValueError('value error: Expecting integers!')

        # The element_dict must be a dictionary
        if not isinstance(element_dict, dict):
            raise ValueError('value error: Expecting a dictionary!')

        # Check if the element already exists or not. If existed, remove everything!
        child = self.elements.search_list(element)
        if child:
            deleted_elements = child[1].delete_object()
            for deleted_element in deleted_elements:
                self.elements.remove_element(deleted_element)

        # Let create the child
        child = self.project_class(
            element,
            element_dict,
            ctime(time()),
            get_int(element_dict.get('timeworked', 0)),
            get_int(element_dict.get('timeestimated', 0)),
            get_int(element_dict.get('timeleft', 0)),
        )

        if parent:
            if not isinstance(parent, int):
                raise ValueError('value error: Expecting integers!')

            # Get parent object
            parent = self.elements.search_list(parent)
            if not parent:
                raise ValueError('Parent not inserted yet!')
            parent[1].add_list_child(child)

        # Well, this child has been created. Just add to fast_search
        self.elements.insert_element(element, child)

        return

    def project_tree(self, element):
        """
        Return the project tree. The format will be as explained in the ProjectObject elements_children_list() function

        :param element: the element integer
        :return: the tree list
        """
        # Element and parent must be integers
        if not isinstance(element, int):
            raise ValueError('value error: Expecting integers!')

        # Get the pointer to the element
        pointer = self.elements.search_list(element)

        # If we found anything, return it. Otherwise, return an empty list
        if pointer:
            return pointer[1].elements_children_list()

        return []


# TODO tests
def get_int(value):
    if isinstance(value, int):
        return value

    if value.find(' minutes') > 0:
        return int(value[:value.find(' minutes')])
    elif value == '0':
        return 0

    raise ValueError("Can't do anything with this value:"+str(value))


# TODO tests
def __get_root_parent(rt_object, element):
    # Get links for this element
    result = get_ticket_links(rt_object, element)
    parent = 0
    for line in result:
        if 'memberof' in line:
            if parent:
                raise ValueError('More than one parent... sorry, but it is not allowed by now :(')
            parent = int(line[1])
    if parent == 0:
        return element
    else:
        return __get_root_parent(rt_object, parent)


# TODO tests
def __insert_into_project_management(rt_object, project_management_object, element, parent=0):
    # TODO this operation takes too long! One possible resolution is:
    # TODO      - get all tickets using only get_ticket_links function
    # TODO      - with all tickets ID, perform only one query for all info of all objects
    # TODO even so, this will take too long... :(
    element_dict = get_list_of_tickets(rt_object, 'id='+str(element))[0]
    project_management_object.add_element(element, parent, element_dict)

    # Get links for this element
    result = get_ticket_links(rt_object, element)
    for line in result:
        if line[0] == 'members':
            __insert_into_project_management(rt_object, project_management_object, int(line[1]), int(element))

    return


# TODO tests
def generate_project_tree(rt_object, project_management_object, element):
    """
    This function will generate the project tree based on an element (ticket ID).
    First, we will try to find the root parent. From there, we will build the entire list.

    NOTE: this function will accept only one parent, by now. If a element has more than one parent, we will
    generate an error.

    :param rt_object:
    :param project_management_object:
    :param element:
    :return: Null
    """
    if not isinstance(element, int):
        raise ValueError('value error: Expecting integers!')

    # Get the list of parents and children. By now, we will only work with this... sorry, folks!
    parent = __get_root_parent(rt_object, element)

    __insert_into_project_management(rt_object, project_management_object, int(parent))

    return


# TODO tests
def get_project_tree(rt_object, project_management_object, element):
    project_tree = project_management_object.project_tree(element)
    if project_tree:
        return project_tree
    else:
        generate_project_tree(rt_object, project_management_object, element)
        return project_management_object.project_tree(element)
