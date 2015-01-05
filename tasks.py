#!/usr/bin/env python
# encoding: utf-8

from base_task import BaseTask, Node

task_data = {
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
}

task = BaseTask(**task_data)
