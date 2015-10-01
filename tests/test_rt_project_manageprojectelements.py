#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
import pytest

from ditic_kanban.rt_projects import ManageProjectElements


def test_add_element():
    project_tree = ManageProjectElements()
    project_tree.add_element(81818, 0, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})

    assert project_tree.elements.list[0][0] == 81818
    assert project_tree.elements.list[0][1].element == 81818
    assert project_tree.elements.list[0][1].element_time_worked == 10
    assert project_tree.elements.list[0][1].element_time_estimated == 20
    assert project_tree.elements.list[0][1].element_time_left == 30

def test_add_element_integers():
    project_tree = ManageProjectElements()
    with pytest.raises(ValueError) as value_error:
        project_tree.add_element('81818', 0, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    assert 'value error: Expecting integers!' in str(value_error)

    with pytest.raises(ValueError) as value_error:
        project_tree.add_element(81819, '81819', {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    assert 'value error: Expecting integers!' in str(value_error)

def test_add_element_parent():
    project_tree = ManageProjectElements()
    project_tree.add_element(81818, 0, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    project_tree.add_element(81819, 81818, {'timeworked': 30, 'timeestimated': 50, 'timeleft': 20})

    assert project_tree.elements.list[0][0] == 81818
    assert project_tree.elements.list[1][0] == 81819
    assert project_tree.elements.list[0][1].children[0].element == 81819
    assert project_tree.elements.list[0][1].project_time_worked == 40
    assert project_tree.elements.list[0][1].project_time_estimated == 70
    assert project_tree.elements.list[0][1].project_time_left == 50

def test_add_element_unknown_parent():
    project_tree = ManageProjectElements()
    with pytest.raises(ValueError) as value_error:
        project_tree.add_element(81819, 81819, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    assert 'Parent not inserted yet!' in str(value_error)

def test_project_tree():
    project_tree = ManageProjectElements()
    project_tree.add_element(81818, 0, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    project_tree.add_element(81819, 81818, {'timeworked': 30, 'timeestimated': 50, 'timeleft': 20})

    response = project_tree.project_tree(81818)
    assert response == [
        81818,
        {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30},
        40,
        70,
        50,
        [
            [
                81819,
                {'timeworked': 30, 'timeestimated': 50, 'timeleft': 20},
                30,
                50,
                20,
                []
            ]
        ]
    ]

def test_project_tree_unknown_element():
    project_tree = ManageProjectElements()
    project_tree.add_element(81818, 0, {'timeworked': 10, 'timeestimated': 20, 'timeleft': 30})
    project_tree.add_element(81819, 81818, {'timeworked': 30, 'timeestimated': 50, 'timeleft': 20})

    response = project_tree.project_tree(3333)
    assert response == []
