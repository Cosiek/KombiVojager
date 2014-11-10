#!/usr/bin/env python
# encoding: utf-8

from tasks import task
from solvers.BruteForce import BruteForceSolver

brutal = BruteForceSolver(task)
brutal.run()

print brutal.get_summary()

