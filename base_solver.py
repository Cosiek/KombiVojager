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

    def get_summary(self):
        if self.best_solution is None:
            return u'Run the solver first'

        txt = (
            '========== {solver_name} ==========\n'
            'run {cycles} cycles for: {search_time}\n'
            'best found solution: {best_solution}\n'
            'distance: {distance}\n'
        )

        return txt.format(
            solver_name=str(self.__class__),
            cycles=self.cycles,
            search_time=self.search_time,
            best_solution=self.best_solution,
            distance=self.best_distance
        )
