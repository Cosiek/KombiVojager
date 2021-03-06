#!/usr/bin/env python
# encoding: utf-8

from random import shuffle

from base_solver import BaseSolver

INF = float('inf')


class PartialSolution(object):
    lower_bound = INF
    upper_bound = INF
    partial_route = []

    done = False

    def __init__(self, partial_route=[]):
        self.partial_route = partial_route

    def build(self, task, ancestor, next_stop):
        self.partial_route = ancestor.partial_route[:]
        self.partial_route.insert(-1, next_stop)
        self.lower_bound = task.get_path_distance(self.partial_route)

        missing_nodes = list(set(task.all_nodes.keys()) - set(self.partial_route))
        if missing_nodes:
            upper_bound_route = (
                self.partial_route[:-1] +
                missing_nodes +
                [self.partial_route[-1],]
            )
            self.upper_bound = task.get_path_distance(upper_bound_route)
        else:
            self.upper_bound = self.lower_bound
            self.done = True


class BoundAndBrakeDeepFitstSearch(BaseSolver):
    deterministic = False  # actually it's distance is deterministic,
                           # but time isn't.

    # helper
    sort_key = lambda self, x: x.upper_bound
    cycles = 0

    def __init__(self, *args, **kwargs):
        super(BoundAndBrakeDeepFitstSearch, self).__init__(*args, **kwargs)
        self.prepare_data()

    def prepare_data(self):
        self.task.node_names_set = set(self.task.all_nodes.keys())

    def run_search(self):
        self.current_best = self.get_random_solution()
        self.current_score = self.task.get_path_distance(self.current_best)

        solution = PartialSolution([self.task.start.name, self.task.finish.name])
        solution.lower_bound = self.current_score

        self.best_upper = solution
        self.to_check = [solution,]

        self.traverse()

        return self.current_best, self.current_score, self.cycles

    def traverse(self):
        while 1:
            try:
                solution = self.to_check.pop()
            except IndexError:
                # all solutions have been checked - this is the end
                break

            # check if this solution is still worth checking
            if not self.is_worth_traversing(solution):
                # if not, then continue...
                continue

            self.cycles += 1
            partials = []
            # iterate over unused stops...
            for stop in self.get_missing_stops(solution):
                # and create partial solutions
                partial = PartialSolution()
                partial.build(self.task, solution, stop)

                # check if this is a full solution...
                if partial.done:
                    # ... and if it is the best so far
                    if partial.lower_bound < self.current_score:
                        self.current_best = partial.partial_route
                        self.current_score = partial.lower_bound
                # if solutions lower bound is lower then current_best, and lower
                # then best partial solutions upper bound...
                elif self.is_worth_traversing(partial):
                    # ...then add it to the list of potential best solutions
                    partials.append(partial)
                # otherwise - forget about it
                else:
                    pass
            partials.sort(key=self.sort_key)
            self.to_check.extend(partials)

    def is_worth_traversing(self, solution):
        return (solution.lower_bound <= self.current_score
                    and solution.lower_bound < self.best_upper.upper_bound)

    def get_missing_stops(self, solution):
        return self.task.node_names_set - set(solution.partial_route)

    def get_random_solution(self):
        route = [n.name for n in self.task.mid_nodes]
        shuffle(route)
        route = [self.task.start.name, ] + route
        route.append(self.task.finish.name)
        return route
