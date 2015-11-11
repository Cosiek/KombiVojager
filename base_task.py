#!/usr/bin/env python
# encoding: utf-8

from itertools import permutations
from math import sqrt, pow


class AssertRouteError(Exception):
    pass


class Node(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class BaseTask(object):
    # base data (needs to be passed to init)
    start = None
    finish = None
    mid_nodes = []
    name = 'base'

    timeout = None

    # distances can be passed, but all missing distances will be calculated
    # uses keys like 'start_node_name:end_node_name'
    # (so no ':' in node names!)
    distances = {}

    # helper data (calculated)
    all_nodes = {}
    is_circle = None

    def __init__(self, **kwargs):
        self.mid_nodes = []
        self.all_nodes = {}
        self.distances = {}

        for key, val in kwargs.items():
            setattr(self, key, val)

        self.is_circle = self.start == self.finish

        self.prepare_data()

    def prepare_data(self):
        # fill all_nodes dict
        self.all_nodes[self.start.name] = self.start
        self.all_nodes[self.finish.name] = self.finish

        for node in self.mid_nodes:
            self.all_nodes[node.name] = node

        # get a list of stop names (including start and finish)
        stop_names = self.all_nodes.keys()

        for a, b in permutations(stop_names, 2):
            key = '%s:%s' % (a, b)
            self.distances[key] = self.calculate_distance(a, b)

    def get_distance(self, a, b):
        key = '%s:%s' % (a, b)
        dist = self.distances.get(key)
        if dist is None:
            dist = self.calculate_distance(a, b)
            self.distances[key] = dist
        return dist

    def calculate_distance(self, a, b):
        node_a = self.all_nodes[a]
        node_b = self.all_nodes[b]

        return sqrt(pow((node_a.x-node_b.x), 2) + pow((node_a.y-node_b.y), 2))

    def get_path_distance(self, path):
        distance = 0
        for i in xrange(1, len(path)):
            distance += self.get_distance(path[i-1], path[i])

        return distance

    def pop_closest_to(self, origin, nodes):
        distance = float('inf')

        i = 0
        closest_idx = 0
        for node_name in nodes:
            d = self.get_distance(origin, node_name)
            if d < distance:
                distance = d
                closest_idx = i
            i += 1

        return nodes.pop(closest_idx)

    def pop_furthest_to(self, origin, nodes):
        distance = 0

        i = 0
        closest_idx = 0
        for node_name in nodes:
            d = self.get_distance(origin, node_name)
            if d > distance:
                distance = d
                closest_idx = i
            i += 1

        return nodes.pop(closest_idx)

    def verify_route(self, route, solver=None):
        # verify start node
        if route[0] != self.start.name:
            raise AssertRouteError(
                    u"Start node of route doesn't match one from task")

        # verify finish node
        if route[-1] != self.finish.name:
            raise AssertRouteError(
                    u"Finish node of route doesn't match one from task")

        # verify if there are any repeted nodes on route
        route_as_set = set(route)
        if (self.start.name != self.finish.name and
                len(route_as_set) != len(route)):
            raise AssertRouteError(u'Some nodes on route are repeted')
        elif len(route_as_set) != len(route):
            raise AssertRouteError(u'Some nodes on route are repeted')

        # verify if all mid nodes are included
        nodes_as_set = set([n.name for n in self.mid_nodes])
        nodes_as_set.add(self.start.name)
        nodes_as_set.add(self.finish.name)

        if nodes_as_set - route_as_set:
            raise AssertRouteError(u'Some nodes are missing from the route (%s)' % solver)

        if route_as_set - nodes_as_set:
            raise AssertRouteError(u'Unknown nodes are included to the route')
