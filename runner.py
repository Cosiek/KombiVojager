#!/usr/bin/env python
# encoding: utf-8

import pkgutil
import sys

from base_solver import BaseSolver
import tasks


class NoSuchTaskException(KeyError):
    pass


def run_solver(solver_class, task):
    """ Run solver for given task """
    solver = solver_class(task)
    solver.run()
    solver.save_solution(cursor)
    print solver.get_summary()


if __name__ == '__main__':
    # get task
    task_name = ' '.join(sys.argv[1:])
    try:
        task = tasks.tasks[task_name]
    except KeyError:
        print >> sys.stderr, (
                'Unknown task name: "%s".\n'
                'This is a list of defined tasks:\n'
                '%s' % (task_name, '\n'.join(tasks.tasks.keys()))
                )
        sys.exit(1)

    # prepare db connection to store results
    from db_manage import connection, cursor

    # iterate over solvers package to find classes of solvers
    for module_tuple in pkgutil.iter_modules(['solvers']):
        module = __import__('solvers.' + module_tuple[1], fromlist=[''])

        for name in dir(module):
            # skip private attributes
            if name.startswith('__'):
                continue

            stuf = getattr(module, name)
            # if something has 'a_solver' attr set to true, assume it is a solver
            # and run it on task. Since BaseSolver also has 'a_solver' set to true
            # it needs to be excluded.
            if getattr(stuf, 'a_solver', False) and not stuf==BaseSolver:
                run_solver(stuf, task)


    # commit and let go of db
    connection.commit()
    connection.close()
