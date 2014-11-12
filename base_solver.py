#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

class RunSolverFirst(Exception):
    pass


class BaseSolver(object):
    task = None

    best_solution = None
    best_distance = float('inf')
    search_time = None
    cycles = 0

    a_solver = True  # just to find solvrs easyer

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
            raise RunSolverFirst(u'Run the solver first')

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

    def save_solution(self, cursor):
        # fail fast
        if self.best_solution is None:
            raise RunSolverFirst(u'Run the solver first')

        # if solver is deterministic - keep only one record in db
        insert_new_record = True
        if getattr(self, 'deterministic', False):
            # check if record for this solver already exists
            cursor.execute(
                    'SELECT * FROM solver_runs WHERE solver=? AND task=?',
                    (str(self.__class__), self.task.name))

            # if it does - overwrite it (might be updated solution)
            if cursor.fetchone():
                sql = ('UPDATE solver_runs SET '
                       'time=?, '
                       'cycles=?, '
                       'solution=?, '
                       'distance=? '
                       'WHERE solver=? '
                       'AND task=?'
                )

                input = (
                    str(self.search_time),
                    str(self.cycles),
                    unicode(self.best_solution),
                    self.best_distance,
                    str(self.__class__),
                    self.task.name,
                )

                insert_new_record = False

        if insert_new_record:
            sql = 'INSERT INTO solver_runs VALUES (NULL, ?, ?, ?, ?, ?, ?)'

            input = (
                str(self.__class__),
                self.task.name,
                str(self.search_time),
                str(self.cycles),
                unicode(self.best_solution),
                self.best_distance,
            )

        cursor.execute(sql, input)
