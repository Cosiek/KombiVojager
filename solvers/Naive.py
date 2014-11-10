#!/usr/bin/env python
# encoding: utf-8

from base_solver import BaseSolver

class NaiveSolver(BaseSolver):
    def run_search(self):
        # get list of mid nodes names
        mid_nodes = []
        for node in self.task.mid_nodes:
            mid_nodes.append(node.name)

        # find node that is closest to start
        closest = self.pop_closest(self.task.start.name, mid_nodes)

        # build solution
        solution = [closest,]
        while mid_nodes:
            closest = self.pop_closest(solution[-1], mid_nodes)
            solution.append(closest)

        # add start and finish to solution
        solution.append(self.task.finish.name)
        solution.insert(0, self.task.start.name)

        # calculate distance
        distance = self.task.get_path_distance(solution)

        return solution, distance, 1

    def pop_closest(self, last, mid_nodes):
        return self.task.pop_closest_to(last, mid_nodes)
