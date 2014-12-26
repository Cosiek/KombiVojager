#!/usr/bin/env python
# encoding: utf-8

from copy import deepcopy
from itertools import permutations

from base_solver import BaseSolver

INF = float('inf')


class State(object):
    array = []
    row_reference = []
    col_reference = []
    lower_band = 0
    parent = None

    deleted_arc = None

    is_active = True

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class LittleSolver(BaseSolver):
    deterministic = True

    def run_search(self):
        # prepare initial data
        reference, cost_array = self.prepare_cost_array()
        initial_data = {
            'array': cost_array,
            'row_reference': reference,
            'col_reference': deepcopy(reference),
        }

        # set initial state
        initial = State(**initial_data)

        # check if route should end at the same spot it began...
        if not self.task.is_circle:
            # ... and adjust initial state if it isn't
            self.non_circle_initial_state(initial)

        states = [initial,]
        active_states = states

        # start search
        cycles = 0
        best_lower_band = INF

        while active_states:
            # rebuild a list of active states
            active_states = [state for state in states if state.is_active]
            cycles += 1

            # get state with lowest lower band
            active_states.sort(key=lambda x: x.lower_band)
            state = active_states[0]

            # check if it has the anwser
            if len(state.array) == 2:
                state.is_active = False
                break

            # divide it further
            substates = self.divide_state(state)

            if len(substates[0].array) == 2:
                state = substates[0]
                break

            # update best found lower band
            best_lower_band = min(best_lower_band, state.lower_band)

            # add new states to list
            states.extend(substates)

            # mark state as inactive
            state.is_active = False

        arcs = self.get_last_arcs_from_final_state(state)

        while state:
            if state.deleted_arc:
                arcs.append(state.deleted_arc)
            state = state.parent

        solution = self.combine_into_a_route(arcs)
        distance = self.task.get_path_distance(solution)

        return solution, distance, cycles

    def divide_state(self, state):
        # prepare
        array = deepcopy(state.array)

        row_reference = deepcopy(state.row_reference)
        col_reference = deepcopy(state.col_reference)

        lower_band_a = state.lower_band

        # standarize array
        lower_band_a += self.reduce_rows(array)
        lower_band_a += self.reduce_columns(array)

        lower_band_b = lower_band_a

        # find 0 cell with largest cost of removal
        lb, cell_cords = self.find_cell_for_removal(array)
        lower_band_b += lb

        # remove coresponding cells from references
        # they will be attached to state a as arc to follow
        node1 = row_reference.pop(cell_cords[0])
        node2 = col_reference.pop(cell_cords[1])

        # remove cell
        self.remove_row(cell_cords[0], array)
        self.remove_column(cell_cords[1], array)

        # block returning path
        self.block_sub_cycles(array, node1, node2, col_reference,
                row_reference, state)

        # calculate new lower band for the array with deleted cell
        lower_band_a += self.reduce_rows(array)
        lower_band_a += self.reduce_columns(array)

        # prepare array for state that rejects found arc
        state_b_array = deepcopy(state.array)
        state_b_array[cell_cords[0]][cell_cords[1]] = self.get_big_number(
                state.array)

        # generate states
        state_a = State(array=array, row_reference=row_reference,
                col_reference=col_reference, lower_band=lower_band_a,
                parent=state, deleted_arc=(node1, node2))
        state_b = State(array=state_b_array,
                row_reference=deepcopy(state.row_reference),
                col_reference=deepcopy(state.col_reference),
                lower_band=lower_band_b, parent=state)

        return state_a, state_b

    def block_sub_cycles(self, array, node1, node2, col_reference,
            row_reference, state):
        # get all included arcs from parent states
        arcs = []
        parent = state
        while parent:
            if parent.deleted_arc:
                arcs.append(parent.deleted_arc)
            parent = parent.parent

        # combine arcs into subroutes
        def combine_arcs(base_arc, arcs):
            route = list(base_arc)
            while arcs:
                break_out = True
                for i, arc in enumerate(arcs):
                    if arc[0] == route[-1]:
                        route.append(arc[1])
                        break_out = False
                        del arcs[i]
                    elif arc[1] == route[0]:
                        route.insert(0, arc[0])
                        break_out = False
                        del arcs[i]

                if break_out:
                    break

            return route

        subroutes = []
        while arcs:
            arc = arcs.pop()
            subroutes.append(combine_arcs(arc, arcs))

        # block return path of every subroute
        for subroute in subroutes:
            try:
                start_idx = col_reference.index(subroute[0])
                end_idx = row_reference.index(subroute[-1])
                array[end_idx][start_idx] = INF
            except ValueError:
                pass


    def find_cell_for_removal(self, array):
        cell_cords = (0, 0)
        max_cost = 0

        for i, row in enumerate(array):
            for j, value in enumerate(row):
                if value == 0:
                    cost = self.get_min_except_one_0(row)
                    col = [r[j] for r in array]
                    cost += self.get_min_except_one_0(col)

                    if cost > max_cost:
                        max_cost = cost
                        cell_cords = (i, j)

        return max_cost, cell_cords

    def get_min_except_one_0(self, array):
        result = INF
        zero_found = False
        for v in array:
            if v != 0:
                result = min(result, v)
            elif v == 0 and zero_found:
                result = 0
                break
            else:
                zero_found = True
        return result

    def get_last_arcs_from_final_state(self, state):
        # get last two arcs from state with 2x2 array
        col_idx_1 = state.array[0].index(0)
        col_idx_2 = state.array[1].index(0)

        arc_1 = state.row_reference[0], state.col_reference[col_idx_1]
        arc_2 = state.row_reference[1], state.col_reference[col_idx_2]

        return [arc_1, arc_2]

    def combine_into_a_route(self, arcs):
        route = [self.task.start.name, ]

        while len(route) < len(arcs):
            for arc in arcs:
                if arc[0] == route[-1]:
                    route.append(arc[1])
                    break

        return route

    def get_big_number(self, array):
        # retutn sum of all positive, non infiniet numbers in array
        return sum(sum([i for i in row if i > 0 and i < INF]) for row in array) + 1

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

    def non_circle_initial_state(self, state):
        """
        Adjust initial state as if arc finish -> start ia already selected
        """
        start = self.task.start.name
        end = self.task.finish.name
        # set states deleted_arc
        state.deleted_arc = (end, start)
        # get indexes of start and end nodes
        start_idx = state.col_reference.index(start)
        end_idx = state.row_reference.index(end)
        # delete nodes from references
        state.col_reference.pop(start_idx)
        state.row_reference.pop(end_idx)
        # block start > connection
        state.array[start_idx][end_idx] = INF
        # delete column and row from states array
        self.remove_row(end_idx, state.array)
        self.remove_column(start_idx, state.array)

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

    def remove_column(self, col_idx, array):
        for row in array:
            del row[col_idx]

    def remove_row(self, row_idx, array):
        del array[row_idx]
