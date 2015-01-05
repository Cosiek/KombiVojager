#!/usr/bin/env python
# encoding: utf-8


INF = float('inf')

def print_array(array):
    print '-----'
    for row in array:
        print [int(x) if isinstance(x, float) and x < INF else x for x in row]

# Timeout --------------------------------------------------------------------

class TimeoutError(Exception):
    pass
