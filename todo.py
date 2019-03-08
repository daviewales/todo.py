#!/usr/bin/env python3

# todo.py

# Create and manage an ordered list of tasks.
# Tasks may be added either to the start or the end of the list.
# Tasks are stored in yaml format.

from pathlib import Path
from yaml import safe_load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def write_tasks(tasks, todo_file):
    '''Write tasks to file

    >>> todo_file = Path('./test_todo.yml')
    >>> tasks = []
    >>> write_tasks(tasks, todo_file)
    >>> load_tasks(todo_file)
    []
    >>> todo_file = Path('./test_todo.yml')
    >>> tasks = ['Eat', 'Sleep', 'Clean', 'Exercise']
    >>> write_tasks(tasks, todo_file)
    >>> load_tasks(todo_file)
    ['Eat', 'Sleep', 'Clean', 'Exercise']
    '''

    with open(todo_file, 'w') as file:
        dump(tasks, file, default_flow_style=False)


def load_tasks(todo_file):
    '''Load tasks from file.

    >>> todo_file = Path('./test_todo.yml')
    >>> load_tasks(todo_file)
    ['Eat', 'Sleep', 'Clean', 'Exercise']
    '''

    with open(todo_file, 'r') as file:
        return safe_load(file)


def add_task_to_beginning(task, tasks):
    '''Add task to beginning of list, to do now.

    >>> tasks = ['Eat', 'Sleep']
    >>> task = 'Clean'
    >>> add_task_to_beginning(task, tasks)
    >>> tasks
    ['Clean', 'Eat', 'Sleep']
    '''

    tasks.insert(0, task)


def add_task_to_end(task, tasks):
    '''Add task to end of list, to do later.

    >>> tasks = ['Eat', 'Sleep']
    >>> task = 'Clean'
    >>> add_task_to_end(task, tasks)
    >>> tasks
    ['Eat', 'Sleep', 'Clean']
    '''

    tasks.append(task)


def delete_task(task_index, tasks):
    '''Delete and return task with specified index

    >>> tasks = ['Eat', 'Sleep', 'Clean']
    >>> delete_task(0, tasks)
    'Eat'
    >>> tasks == ['Sleep', 'Clean']
    True
    '''

    return tasks.pop(task_index)


def list_tasks(tasks, n=3, all_tasks=False, from_beginning=True):
    '''List n tasks. Defaults to n=3, starting from the most current task

    >>> tasks = ['Eat', 'Sleep', 'Clean', 'Exercise']
    >>> list_tasks(tasks)
    ['Eat', 'Sleep', 'Clean']
    >>> list_tasks(tasks, n=2)
    ['Eat', 'Sleep']
    >>> list_tasks(tasks, all_tasks=True)
    ['Eat', 'Sleep', 'Clean', 'Exercise']
    >>> list_tasks(tasks, from_beginning=False)
    ['Exercise', 'Clean', 'Sleep']
    >>> list_tasks(tasks, n=10)
    ['Eat', 'Sleep', 'Clean', 'Exercise']
    >>> list_tasks(tasks, n=10, from_beginning=False)
    ['Exercise', 'Clean', 'Sleep', 'Eat']
    '''

    if all_tasks:
        n = len(tasks)

    if from_beginning:
        return tasks[:n]
    else:
        return tasks[-1:-n-1:-1]


def current_task(tasks):
    '''Return the current task
    
    >>> tasks = ['Eat', 'Sleep']
    >>> current_task(tasks)
    'Eat'
    >>> tasks = []
    >>> current_task(tasks)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    '''

    try:
        return tasks[0]
    except IndexError as err:
        print('The task list is empty!')
        raise err


def main():
    tasks = ['Eat', 'Sleep']
    print(current_task(tasks))


if __name__ == '__main__':
    main()
