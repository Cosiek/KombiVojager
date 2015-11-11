#!/usr/bin/env python
# encoding: utf-8

from base_task import BaseTask, Node

task_definitions = [
    {
        'name': 'first_test_runs_task',
        'start': Node('A', 0, 0),
        'finish': Node('Z', 500, 500),
        'mid_nodes': [
            Node('B', 50, 500),
            Node('C', 50, 100),
            Node('D', 0, 550),
            Node('E', 500, 100),
            Node('F', 250, 250),
            Node('G', 150, 400),
            Node('H', 350, 150),
        ],
        'distances': {
            'A:B': 10,
        },
        'timeout': 1,
    },
    {
        'name': 'test_task_symetric_distances_only',
        'start': Node('A', 0, 0),
        'finish': Node('Z', 500, 500),
        'mid_nodes': [
            Node('B', 50, 500),
            Node('C', 50, 100),
            Node('D', 0, 550),
            Node('E', 500, 100),
            Node('F', 250, 250),
            Node('G', 150, 400),
            Node('H', 350, 150),
        ],
        'distances': {
            'A:B': 10,
            'B:A': 10,
            'B:C': 5,
            'C:D': 10,
            'D:E': 30,
            'E:F': 17,
            'F:G': 35,
            'G:H': 40,
            'H:C': 20,
            'F:A': 15,
            'F:C': 5,
            'A:Z': 30,
        },
        'timeout': 10,
        'paths_only': True,
    },
    {
        'name': 'test_task_asymetric_distances_only',
        'start': Node('A', 0, 0),
        'finish': Node('Z', 500, 500),
        'mid_nodes': [
            Node('B', 50, 500),
            Node('C', 50, 100),
            Node('D', 0, 550),
            Node('E', 500, 100),
            Node('F', 250, 250),
            Node('G', 150, 400),
            Node('H', 350, 150),
        ],
        'distances': {
            'A:B': 10,
            'B:C': 5,
            'C:D': 10,
            'D:E': 30,
            'E:F': 17,
            'F:G': 35,
            'G:H': 40,
            'H:C': 20,
            'F:A': 15,
            'F:C': 5,
            'F:Z': 1,
        },
        'timeout': 1,
        'paths_only': True,
        'symetric': False,
    },
]


tasks = {}
for task_def in task_definitions:
    tasks[task_def['name']] = BaseTask(**task_def)
