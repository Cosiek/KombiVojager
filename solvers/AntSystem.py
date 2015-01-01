#!/usr/bin/env python
# encoding: utf-8

from random import shuffle, random
from itertools import permutations

from base_solver import BaseSolver


INF = float('inf')


class Ant(object):
    route = []
    score = INF

    def __init__(self, route):
        self.route = route

    def evaluate(self, task):
        start = task.start.name
        finish = task.finish.name

        route = [start, ] + self.route + [finish, ]
        self.score = task.get_path_distance(route)

    def update_trail(self, total_distance, arcs, start, finish):
        power = self.score / total_distance

        # update arcs on route
        for i in range(1, len(self.route)):
            arc = (self.route[i-1], self.route[i])
            arcs[arc] += power

        # remember to update begining and end arcs
        arcs[(start, self.route[0])] += power
        arcs[(self.route[0], finish)] += power

    def run(self, arcs, start):
        route = [start,]
        unused_nodes = set(self.route)

        # use shuffled arcs list to prevent privleged arcs
        shuffled_arcs = arcs.keys()
        shuffle(shuffled_arcs)

        while unused_nodes:
            power_from_origin = 0.0
            tmp_arcs = {}
            for arc, power in arcs.iteritems():
                if arc[0] == route[-1] and arc[1] in unused_nodes:
                    tmp_arcs[arc] = power
                    power_from_origin += power

            n = random()

            for arc, power in tmp_arcs.items():
                if power_from_origin == 0:
                    break
                elif power / power_from_origin > n:
                    break

            route.append(arc[1])
            unused_nodes.remove(arc[1])

        self.route = route[1:]


class AntSystemSolver(BaseSolver):
    deterministic = False

    # genetic alghoritm settings
    ants_count = 50
    vaporize_factor = 0.5

    # helpers
    best_route = []
    best_score = INF

    def run_search(self):
        # TODO - adjust settings acording to preblems complexity
        # genetate some random solutions
        self.ants = self.generate_initial_ants(self.task)
        # prepare data for pheromone trails
        self.prepare_arcs()
        # check stop condition (run loop)
        self.cycles = 0
        while self.continue_():
            # evaluate each ants solution
            self.evaluate_ants()

            # get all the best
            self.update_best_solutions()

            # update pheromone trail
            self.update_pheromone_trails()

            self.vaporize()
            # release the ants
            self.run_ants()

            self.cycles += 1


        route = ([self.task.start.name] + self.best_route +
                [self.task.finish.name])
        return route, self.best_score, self.cycles

    def generate_initial_ants(self, task):
        nodes = [node.name for node in task.mid_nodes]
        ants = []
        for i in range(self.ants_count):
            route = nodes[:]
            shuffle(route)

            ants.append(Ant(route))

        return ants

    def prepare_arcs(self):
        nodes = self.task.all_nodes.keys()
        self.arcs = {x: 0 for x in permutations(nodes, 2)}

    def continue_(self):
        return self.cycles <= 100

    def evaluate_ants(self):
        for ant in self.ants:
            ant.evaluate(self.task)

    def update_pheromone_trails(self):
        total_distance = 0
        for ant in self.ants:
            total_distance += ant.score

        start = self.task.start.name
        finish = self.task.finish.name

        for ant in self.ants:
            ant.update_trail(total_distance, self.arcs, start, finish)

    def vaporize(self):
        for arc, power in self.arcs.iteritems():
            if power:
                self.arcs[arc] = self.get_vaporized_power(power)

    def get_vaporized_power(self, power):
        return max(0, power * self.vaporize_factor)

    def run_ants(self):
        start = self.task.start.name
        for ant in self.ants:
            ant.run(self.arcs, start)

    def update_best_solutions(self):
        for ant in self.ants:
            if ant.score < self.best_score:
                self.best_score = ant.score
                self.best_route = ant.route
