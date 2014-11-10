#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

class BaseSolver(object):
    task = None

    best_solution = None
    best_distance = float('inf')
    search_time = None
    cycles = 0

    def __init__(self, task):
        self.task = task

    def run(self):
        start_time = datetime.now()
        self.best_solution, self.best_distance, self.cycles = self.run_search()
        finish_time = datetime.now()

        self.search_time = finish_time - start_time

    def run_search(self):
        # dummy - this is where one should implement the algorithm
        pass
