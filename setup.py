# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ditic_kanban',
    version='0.1',
    description='Dashboard Kanban for DITIC',
    url='http://www.uc.pt/',
    author='Pedro Vapi',
    author_email='vapi@uc.pt',
    license='MIT',
    packages=['ditic_kanban'],
    install_requires=['bottle', 'pytest', 'paste'],
    entry_points={
        'console_scripts': [
            'ditic_kanban_server = ditic_kanban.server:start_server',
            'generate_summary_file = ditic_kanban.rt_summary:generate_summary_file',
            'get_summary_info = ditic_kanban.rt_summary:get_summary_info',
            'update_statistics = ditic_kanban.statistics:stats_update_json_file',
        ]
    }
)
