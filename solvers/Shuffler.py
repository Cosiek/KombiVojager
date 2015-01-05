#!/usr/bin/env python
# encoding: utf-8

from base_solver import BaseSolver


class ShuffleClosestFirstSolver(BaseSolver):
    deterministic = True

    def run_search(self):
        mid_nodes = []
        for node in self.task.mid_nodes:
            mid_nodes.append(node.name)

        # init solution
        solution = [self.task.start.name, self.task.finish.name]
        cycles = 0
        while mid_nodes:
            # get next node to insert into solution
            node = self.pop_node(solution[-1], mid_nodes)

            # try to put this node in best position on the solution
            distance = float('inf')
            idx = 0
            for i in range(len(solution)-1):
                s = solution[:i + 1]
                s.append(node)
                s += solution[i + 1:]

                d = self.task.get_path_distance(s)
                if d < distance:
                    distance = d
                    idx = i + 1

                cycles +=1

            # apply node to solution at given index
            solution.insert(idx, node)

            self.check_timeout()

        return solution, distance, cycles

    def pop_node(self, last, mid_nodes):
        return self.task.pop_closest_to(last, mid_nodes)


class ShuffleFurtherFirstSolver(ShuffleClosestFirstSolver):
    def pop_node(self, last, mid_nodes):
        return self.task.pop_furthest_to(last, mid_nodes)
