#!/usr/bin/env python
# encoding: utf-8

from random import shuffle, random, randint

from base_solver import BaseSolver


INF = float('inf')


class Solution(object):
    route = []
    score = INF

    fixed = False
    evaluated = False

    def __init__(self, route):
        self.route = route

    def crossing(self, other):
        # choose a node that will be the cut
        cut_idx = randint(1, len(self.route) - 2)
        node = self.route[cut_idx]
        # find this nodes position on other route
        other_cut_idx = other.route.index(node)
        # glue new routes from pieces of old routes
        new_route_1 = self.route[:cut_idx] + other.route[other_cut_idx:]
        new_route_2 = other.route[:other_cut_idx] + self.route[cut_idx:]
        # create new solutions
        child1 = Solution(new_route_1)
        child2 = Solution(new_route_2)

        return child1, child2

    def mutation(self):
        node = self.route.pop(randint(0, len(self.route) - 1))
        self.route.insert(randint(0, len(self.route)), node)
        self.evaluated = False

    def fix(self, task, mid_nodes):
        # don't fix solution multiple times
        if self.fixed:
            return

        # prepare helper sets
        route_set = set(self.route)
        missing = mid_nodes - route_set
        # remove all repeted nodes from route
        route = []
        for node in self.route:
            if node in route_set:
                route.append(node)
                route_set.remove(node)

        # make sure all needed nodes are included
        start = [task.start.name, ]
        finish = [task.finish.name, ]
        for node in missing:
            distance = INF
            best_route = route
            i = 0
            # find a best place to fit this node
            while i <= len(route):
                test_route = start + route[:i] + [node, ] + route[i:] + finish
                route_dist = task.get_path_distance(test_route)
                if distance > route_dist:
                    distance = route_dist
                    best_route = test_route
                i += 1
            route = best_route[1:-1]

        self.route = route
        self.fixed = True


class GeneticSolver(BaseSolver):
    deterministic = False

    # genetic alghoritm settings
    population_count = 30
    mutation_ratio = 1/30

    # helpers
    sort_key = lambda self, x: x.score

    def run_search(self):
        # prepare data
        self.generation = 0

        best_score = INF
        best_route = None

        self.chromosomes = set([mn.name for mn in self.task.mid_nodes])

        # generate initial population
        self.population = self.generate_initial_population(self.chromosomes)

        # evaluate solutions
        self.evaluate_solutions()

        # check finish condition
        while self.continue_():
            # apply crossing
            self.crossing()

            # apply mutation
            self.mutation()

            # fix wrong solutions
            self.fix_solutions()

            # evaluate solutions
            self.evaluate_solutions()

            # sort solutions
            self.population.sort(key=self.sort_key)

            # limit population
            self.population = self.population[:self.population_count]

            # update best
            if self.population[0].score < best_score:
                best = self.population[0]
                best_score, best_route = best.score, best.route[:]

            self.generation += 1

        return best_route, best_score, self.generation

    def generate_initial_population(self, chromosomes):
        population = []
        for i in range(self.population_count):
            route = list(chromosomes)
            shuffle(route)

            solution = Solution(route)
            population.append(solution)

        return population

    def evaluate_solutions(self):
        start = self.task.start.name
        finish = self.task.finish.name
        for solution in self.population:
            if not solution.evaluated:
                route = [start, ] + solution.route + [finish, ]
                solution.score = self.task.get_path_distance(route)
                solution.evaluated = True

    def continue_(self):
        return self.generation <= 100

    def fix_solutions(self):
        for solution in self.population:
            solution.fix(self.task, self.chromosomes)

    def mutation(self):
        for solution in self.population:
            if self.mutation_ratio >= random():
                solution.mutation()

    def crossing(self):
        # the shorter is solutions route, the more probable that it will
        # be selected.
        t = 0
        for solution in self.population:
            t += 1 / solution.score

        # choose population/2 pairs of solutions for crossing
        def choose_solution():
            rend = random() * t
            o = 0
            for j, solution in enumerate(self.population):
                o += 1/solution.score
                if o > rend:
                    break

            return j, solution

        new_generation = []
        for i in range(int(self.population_count)):
            idx1, solution1 = choose_solution()
            idx2, solution2 = choose_solution()

            if idx1 != idx2:
                children = solution1.crossing(solution2)
                new_generation.extend(children)

        # update population with new solutions
        self.population.extend(new_generation)
