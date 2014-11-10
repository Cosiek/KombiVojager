#!/usr/bin/env python
# encoding: utf-8

from tasks import task
from db_manage import connection, cursor

from solvers.BruteForce import BruteForceSolver
from solvers.Naive import NaiveSolver


brutal = BruteForceSolver(task)
brutal.run()
brutal.save_solution(cursor)
print brutal.get_summary()

naive = NaiveSolver(task)
naive.run()
naive.save_solution(cursor)
print naive.get_summary()

connection.commit()
connection.close()
