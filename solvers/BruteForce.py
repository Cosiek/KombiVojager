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
        best_distance = float('inf')
        best_solution = None
        cycles = 0
        for permutation in permutations(mid_nodes):
            # check permutation distance
            path = [self.task.start.name, ]
            path.extend(permutation)
            path.append(self.task.finish.name)
            distance = self.task.get_path_distance(path)

            # check if this is the best solution so far
            if distance < best_distance:
                best_distance = distance
                best_solution = path

            cycles += 1

        return best_solution, best_distance, cycles
