#!/usr/bin/env python
# encoding: utf-8

from tasks import task
from solvers.BruteForce import BruteForceSolver
from solvers.Naive import NaiveSolver

brutal = BruteForceSolver(task)
brutal.run()
print brutal.get_summary()

naive = NaiveSolver(task)
naive.run()
print naive.get_summary()
