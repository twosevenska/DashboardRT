#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This file contains several functions that do several operations necessary to this package to work
#
import pytest

from ditic_kanban.rt_projects import ProjectElementFastSearch

def test_insert_element():
    search = ProjectElementFastSearch()
    # Simulate that the list is already ordered
    search.is_ordered = True

    search.insert_element(81818, 'test')

    assert search.list == [[81818, 'test']]
    assert search.is_ordered == False

def test_insert_element_not_ok():
    search = ProjectElementFastSearch()
    with pytest.raises(ValueError) as value_error:
        search.insert_element('81818', 'Test')
    assert 'value error: Expecting integers!' in str(value_error)

def test_search_list_odd_elements():
    search = ProjectElementFastSearch()
    search.insert_element(81818, 'test 81818')
    search.insert_element(81819, 'test 81819')
    search.insert_element(81820, 'test 81820')

    response = search.search_list(81818)
    assert response == [81818, 'test 81818']

    response = search.search_list(81819)
    assert response == [81819, 'test 81819']

    response = search.search_list(81820)
    assert response == [81820, 'test 81820']

    response = search.search_list(81830)
    assert response == []

    response = search.search_list(81810)
    assert response == []

def test_search_list_even_elements():
    search = ProjectElementFastSearch()
    search.insert_element(81818, 'test 81818')
    search.insert_element(81819, 'test 81819')
    search.insert_element(81820, 'test 81820')
    search.insert_element(81821, 'test 81821')

    response = search.search_list(81818)
    assert response == [81818, 'test 81818']

    response = search.search_list(81819)
    assert response == [81819, 'test 81819']

    response = search.search_list(81820)
    assert response == [81820, 'test 81820']

    response = search.search_list(81821)
    assert response == [81821, 'test 81821']

    response = search.search_list(81830)
    assert response == []

    response = search.search_list(81810)
    assert response == []

def test_search_list_one_element():
    search = ProjectElementFastSearch()
    search.insert_element(81818, 'test 81818')

    response = search.search_list(81818)
    assert response == [81818, 'test 81818']

    response = search.search_list(81810)
    assert response == []

def test_search_list_unsorted():
    search = ProjectElementFastSearch()
    search.insert_element(81819, 'test 81819')
    search.insert_element(81821, 'test 81821')
    search.insert_element(81820, 'test 81820')
    search.insert_element(81818, 'test 81818')

    response = search.search_list(81818)
    assert response == [81818, 'test 81818']

    response = search.search_list(81819)
    assert response == [81819, 'test 81819']

    response = search.search_list(81820)
    assert response == [81820, 'test 81820']

    response = search.search_list(81821)
    assert response == [81821, 'test 81821']

    response = search.search_list(81830)
    assert response == []

    response = search.search_list(81810)
    assert response == []

def test_remove_element():
    search = ProjectElementFastSearch()
    search.insert_element(81819, 'test 81819')
    search.insert_element(81821, 'test 81821')
    search.insert_element(81820, 'test 81820')

    search.remove_element(81819)
    assert search.list == [
        [81820, 'test 81820'],
        [81821, 'test 81821'],
    ]