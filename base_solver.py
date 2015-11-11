#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime, timedelta

from helpers import TimeoutError, INF


class RunSolverFirst(Exception):
    pass


class BaseSolver(object):
    task = None

    best_solution = None
    best_distance = float('inf')
    search_time = None
    cycles = 0

    a_solver = True  # just to find solvrs easier

    # timeout related
    timedout = False

    time_to_get_out = None
    start_time = None

    def __init__(self, task):
        self.task = task

    def run(self):
        self.start_time = datetime.now()
        try:
            self.best_solution, self.best_distance, self.cycles = self.run_search()
        except TimeoutError:
            self.handle_timeout()
        finish_time = datetime.now()
        self.search_time = finish_time - self.start_time

        self.task.verify_route(self.best_solution, self)

    def run_search(self):
        # dummy - this is where one should implement the algorithm
        # this should include calls to self.check_timeout
        pass

    def check_timeout(self):
        if self.time_to_get_out:
            if self.time_to_get_out < datetime.now():
                self.timedout = True
                raise TimeoutError
        elif self.task.timeout:
            self.time_to_get_out = self.start_time + timedelta(
                    seconds=self.task.timeout)

    def handle_timeout(self):
        # this can vary a lot between diffrent algorithms
        # (it may be usefull to get best solution found till now)
        self.cycles = 0
        self.best_solution = []
        self.best_distance = INF

    def get_summary(self):
        if self.best_solution is None and not self.timedout:
            raise RunSolverFirst(u'Run the solver first')

        if self.timedout and self.best_solution:
            txt = (
                '========== {solver_name} ==========\n'
                '*            TIMEDOUT            *\n'
                'run {cycles} cycles for: {search_time}\n'
                'best found solution: {best_solution}\n'
                'distance: {distance}\n'
            )
        elif self.timedout:
            txt = (
                '========== {solver_name} ==========\n'
                'TIMEDOUT after {search_time}\n'

            )
        else:
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
        if self.best_solution is None and not self.timedout:
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
                       'distance=?, '
                       'timedout=? '
                       'WHERE solver=? '
                       'AND task=?'
                )

                input = (
                    str(self.search_time),
                    str(self.cycles),
                    unicode(self.best_solution),
                    self.best_distance,
                    self.timedout,
                    str(self.__class__),
                    self.task.name,
                )

                insert_new_record = False

        if insert_new_record:
            sql = 'INSERT INTO solver_runs VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)'

            input = (
                str(self.__class__),
                self.task.name,
                str(self.search_time),
                str(self.cycles),
                unicode(self.best_solution),
                self.best_distance,
                self.timedout,
            )

        cursor.execute(sql, input)
