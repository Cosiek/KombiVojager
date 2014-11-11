#!/usr/bin/env python
# encoding: utf-8

from tasks import task
from db_manage import connection, cursor

from solvers.BruteForce import BruteForceSolver
from solvers.Naive import NaiveSolver
from solvers.Shuffler import ShuffleSolver


brutal = BruteForceSolver(task)
brutal.run()
brutal.save_solution(cursor)
print brutal.get_summary()

naive = NaiveSolver(task)
naive.run()
naive.save_solution(cursor)
print naive.get_summary()

shuffle = ShuffleSolver(task)
shuffle.run()
shuffle.save_solution(cursor)
print shuffle.get_summary()

connection.commit()
connection.close()
