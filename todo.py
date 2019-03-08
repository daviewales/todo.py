#!/usr/bin/env python3

# todo.py

# Create and manage an ordered list of tasks.
# Tasks may be added either to the start or the end of the list.
# Tasks are stored in yaml format.

from pathlib import Path
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def write_tasks(filepath):
    '''Write tasks to file'''
    pass

def load_tasks(filepath):
    '''Load tasks from file.'''
    pass


def add_task_to_beginning(task, tasks):
    '''Add task to beginning of list, to do now.

    >>> tasks = ['Eat', 'Sleep']
    >>> task = 'Clean'
    >>> add_task_to_beginning(task, tasks)
    ['Clean', 'Eat', 'Sleep']
    '''

    tasks.insert(0, task)
    return tasks


def add_task_to_end(task, tasks):
    '''Add task to end of list, to do later.

    >>> tasks = ['Eat', 'Sleep']
    >>> task = 'Clean'
    >>> add_task_to_end(task, tasks)
    ['Eat', 'Sleep', 'Clean']
    '''

    tasks.append(task)
    return tasks

def delete_task(task_index):
    pass

def list_tasks(n=10, all_tasks=False, from_end=True):
    pass

def current_task(tasks):
    '''Return the current task
    
    >>> tasks = ['Eat', 'Sleep']
    >>> current_task(tasks)
    'Eat'
    >>> tasks = []
    >>> current_task(tasks)

    '''

    try:
        return tasks[0]
    except IndexError:
        pass

def main():
    tasks = ['Eat', 'Sleep']
    print(current_task(tasks))

if __name__ == '__main__':
    main()
