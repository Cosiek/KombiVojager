#!/usr/bin/env python
# encoding: utf-8

from copy import deepcopy
from itertools import permutations

from base_solver import BaseSolver

INF = float('inf')

class LittleSolver(BaseSolver):
    deterministic = True

    def run_search(self):
        # prepare cost array
        reference, work_array = self.prepare_cost_array()

        # arrays for reference (keeping names of nodes)
        row_reference = reference
        col_reference = deepcopy(reference)

        # strip down array until it's 2x2 sized
        removed_pairs = []
        cycles = 0
        while len(work_array) > 2:
            # substract row
            self.reduce_rows(work_array)
            # substract column
            self.reduce_columns(work_array)

            # find smallest in row (except 0 if only one)
            smallest_in_rows = self.get_smallest_in_rows(work_array)
            # find smallest in column (except 0 if only one)
            smallest_in_cols = self.get_smallest_in_columns(work_array)

            # get biggest of them all
            big = max(max(smallest_in_rows), max(smallest_in_cols))

            # find column and/or row that has a 0 and biggest in it
            row_idx, col_idx = self.find_indexes_for_reduction(
                    big, work_array)

            # put inf on this column and row crossing
            work_array[col_idx][row_idx] = INF

            # remove this column and row
            self.remove_column(col_idx, work_array)
            self.remove_row(row_idx, work_array)

            # remember delated arc
            removed_pairs.append(
                    [row_reference.pop(row_idx), col_reference.pop(col_idx)]
            )

            cycles += 1

        # add missing arcs, based on current work array
        removed_pairs.append(
                self.get_missing_pair(work_array, row_reference, col_reference))
        removed_pairs.append((row_reference.pop(), col_reference.pop()))

        # combine arcs into a route
        route = self.combine_into_a_route(removed_pairs)

        # calculate route distance
        distance = self.task.get_path_distance(route)

        return route, distance, cycles


    def prepare_cost_array(self):
        # get nodes names
        reference = self.task.all_nodes.keys()
        len_ref = len(reference)

        # prepare array filled with infinity
        array = [[INF,] * len_ref for i in range(len_ref)]

        # fill array with distances
        for pair in permutations(range(len_ref), 2):
            node_a = reference[pair[0]]
            node_b = reference[pair[1]]

            array[pair[0]][pair[1]] = self.task.get_distance(node_a, node_b)

        return reference, array

    def reduce_rows(self, array):
        lb = 0
        for i, row in enumerate(array):
            m = min(row)
            lb += m
            array[i] = [x - m for x in row]

        return lb

    def reduce_columns(self, array):
        lb = 0
        for i in range(len(array)):
            m = min([row[i] for row in array])
            lb += m
            for row in array:
                row[i] -= m

        return lb

    def get_smallest_in_rows(self, array):
        # use 0 only if present more then once in row
        smallest_list = []

        # fill list of smallest values in each row
        for row in array:
            zero_found = False
            smallest = INF
            for cell in row:
                if cell == 0 and zero_found:
                    smallest = 0
                    break
                elif cell == 0:
                    zero_found = True
                elif cell < smallest:
                    smallest = cell

            smallest_list.append(smallest)

        return smallest_list

    def get_smallest_in_columns(self, array):
        # use 0 only if present more then once in column
        smallest_list = []

        # fill list of smallest values in each column
        for i in range(len(array)):
            col = [row[i] for row in array]
            zero_found = False
            smallest = INF
            for cell in col:
                if cell == 0 and zero_found:
                    smallest = 0
                    break
                elif cell == 0:
                    zero_found = True
                elif cell < smallest:
                    smallest = cell

            smallest_list.append(smallest)

        return smallest_list

    def find_indexes_for_reduction(self, big, work_array):
        # find row_idx, col_idx pairs for cells that contain big value
        pairs = self.find_cells_of_value(big, work_array)

        # for each pair find first column or row that has a 0 in it
        row_idx = None
        col_idx = None
        for row_idx, col_idx in pairs:
            # check column
            for i in range(len(work_array)):
                if work_array[i][col_idx] == 0:
                    row_idx = i
                    break

            # check row
            if 0 in work_array[row_idx]:
                col_idx = work_array[row_idx].index(0)
                break

        return row_idx, col_idx

    def find_cells_of_value(self, val, array):
        result = []
        for row_idx, row in enumerate(array):
            for col_idx, cell_val in enumerate(row):
                if cell_val == val:
                    result.append((row_idx, col_idx))

        return result

    def remove_column(self, col_idx, array):
        for row in array:
            del row[col_idx]

    def remove_row(self, row_idx, array):
        del array[row_idx]

    def get_missing_pair(self, array, row_reference, col_reference):
        for i, row in enumerate(array):
            if 0 in row:
                row_idx = row_reference.pop(i)
                col_idx = col_reference.pop(row.index(0))

        return row_idx, col_idx

    def combine_into_a_route(self, pairs):
        route = [self.task.start.name, ]

        while len(route) < len(pairs):
            for pair in pairs:
                if pair[0] == route[-1]:
                    route.append(pair[1])
                    break

        return route

