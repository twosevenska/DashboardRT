#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
import pytest

from ditic_kanban.rt_projects import ProjectObject


def test_projectobject_ok():
    element = ProjectObject(81818, 'Testing', '2015-07-31', 60, 100, 40)

    assert element.element == 81818
    assert element.ticket_list == 'Testing'
    assert element.update_time == '2015-07-31'
    assert element.element_time_worked == 60
    assert element.element_time_estimated == 100
    assert element.element_time_left == 40
    assert element.project_time_worked == 60
    assert element.project_time_estimated == 100
    assert element.project_time_left == 40
    assert element.bst_left == ''
    assert element.bst_right == ''
    assert element.children == []

def test_projectobject_check_int():
    with pytest.raises(ValueError) as value_error:
        ProjectObject('81818', 'Testing', '2015-07-31', 60, 100, 40)
    assert 'value error: Expecting integers!' in str(value_error)

    with pytest.raises(ValueError) as value_error:
        ProjectObject(81818, 'Testing', '2015-07-31', '60', 100, 40)
    assert 'value error: Expecting integers!' in str(value_error)

    with pytest.raises(ValueError) as value_error:
        ProjectObject(81818, 'Testing', '2015-07-31', 60, '100', 40)
    assert 'value error: Expecting integers!' in str(value_error)

    with pytest.raises(ValueError) as value_error:
        ProjectObject(81818, 'Testing', '2015-07-31', 60, 100, '40')
    assert 'value error: Expecting integers!' in str(value_error)

def test_add_list_child():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)
    element_child1 = ProjectObject(81821, 'Testing3', '2015-07-31', 30, 40, 10)

    element_father.add_list_child(element_child)
    element_child.add_list_child(element_child1)

    assert len(element_father.children) == 1
    assert element_father.children[0].children[0].element == 81821
    assert element_father.project_time_worked == 100
    assert element_father.project_time_estimated == 170
    assert element_father.project_time_left == 70

def test_update_project_times():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)

    element_father.add_list_child(element_child)

    element_child.project_time_worked = 30
    element_child.project_time_estimated = 70
    element_child.project_time_left = 40

    element_father.update_project_times()

    assert element_father.project_time_worked == 90
    assert element_father.project_time_estimated == 170
    assert element_father.project_time_left == 80

def test_elements_children_list():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)

    element_father.add_list_child(element_child)

    result = element_father.elements_children_list()
    assert result == [
        81818,
        'Testing1',
        70,
        130,
        60,
        [
            [
                81820,
                'Testing2',
                10,
                30,
                20,
                []
            ]
        ]
    ]

def test_delete_object():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)
    element_child1 = ProjectObject(81821, 'Testing3', '2015-07-31', 30, 40, 10)

    element_father.add_list_child(element_child)
    element_child.add_list_child(element_child1)

    response = element_father.delete_object()

    assert len(element_father.children) == 0
    assert len(element_child.children) == 0
    assert response == [
        81818,
        81820,
        81821,
    ]

def test_delete_object1():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)
    element_child1 = ProjectObject(81821, 'Testing3', '2015-07-31', 30, 40, 10)
    element_child2 = ProjectObject(81822, 'Testing4', '2015-07-31', 30, 40, 10)

    element_father.add_list_child(element_child)
    element_child.add_list_child(element_child1)
    element_child1.add_list_child(element_child2)

    response = element_child1.delete_object()

    assert len(element_father.children) == 1
    assert element_father.children[0].element == element_child.element
    assert len(element_child.children) == 0
    assert element_child1.parent == ''
    assert response == [
        81821,
        81822,
    ]


def test_remove_child():
    element_father = ProjectObject(81818, 'Testing1', '2015-07-31', 60, 100, 40)
    element_child = ProjectObject(81820, 'Testing2', '2015-07-31', 10, 30, 20)
    element_child1 = ProjectObject(81821, 'Testing3', '2015-07-31', 30, 40, 10)
    element_child2 = ProjectObject(81822, 'Testing4', '2015-07-31', 30, 40, 10)

    element_father.add_list_child(element_child)
    element_father.add_list_child(element_child1)
    element_father.add_list_child(element_child2)

    element_father.remove_child(81821)

    assert len(element_father.children) == 2
    assert element_father.children[0].element == element_child.element
    assert element_father.children[1].element == element_child2.element
