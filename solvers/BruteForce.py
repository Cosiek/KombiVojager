#!/usr/bin/env python
# encoding: utf-8

from itertools import permutations

from base_solver import BaseSolver

class BruteForceSolver(BaseSolver):
    deterministic = True

    def run_search(self):
        # get list of mid nodes names


        mid_nodes = []
        for node in self.task.mid_nodes:
            mid_nodes.append(node.name)

        # iterate over permutations generator
        self.best_distance = float('inf')
        self.best_solution = None
        self.cycles = 0
        for permutation in permutations(mid_nodes):
            # check permutation distance
            path = [self.task.start.name, ]
            path.extend(permutation)
            path.append(self.task.finish.name)
            distance = self.task.get_path_distance(path)

            # check if this is the best solution so far
            if distance < self.best_distance:
                self.best_distance = distance
                self.best_solution = path

            self.cycles += 1

            self.check_timeout()

        return self.best_solution, self.best_distance, self.cycles


    def handle_timeout(self):
        # this alghoritm might produce a solution even if it was timedout
        # and it uses the right variable names
        # so nothing to do here
        pass

