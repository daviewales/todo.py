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


TODO_FILE = Path('~/.todo.yml').expanduser()


def get_args():
    import argparse

    # create top level parser
    parser = argparse.ArgumentParser(description='Manage a todo list.')
    subparsers = parser.add_subparsers(dest='subparser_name', help='View help for sub-commands with "todo.py command -h"')

    # create parser for the 'now' command
    parser_now = subparsers.add_parser('now', aliases=['n'], help='Add task to do now')
    parser_now.add_argument('task', type=str, nargs='+', help='Task to add.') 

    # create parser for the 'later' command
    parser_later = subparsers.add_parser('later', aliases=['l'], help='Add task to do later')
    parser_later.add_argument('task', type=str, nargs='+', help='Task to add.')

    # create parser for the 'list' command
    parser_list = subparsers.add_parser('list', aliases=['ls'], help='List tasks')
    parser_list.add_argument('--all', '-a', action='store_true', help='List all tasks')
    parser_list.add_argument('--from-end', '-e', action='store_true', help='List tasks in reverse order (beginning with lowest priority)')
    parser_list.add_argument('task_count', metavar='N', default=3, nargs='?', type=int, help='Number of tasks to list')

    # create parser for the 'done' command
    parser_done = subparsers.add_parser('done', help='Complete task (defaults to current task)')
    parser_done.add_argument('--interactive', '-i', action='store_true', help='Interactive completion mode. (Useful for completing tasks out of order!)')

    return parser.parse_args()


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


def enumerate_tasks(tasks, n=3, all_tasks=False, from_beginning=True):
    '''Number and list n tasks. Defaults to n=3, starting from the most current task

    >>> tasks = ['Eat', 'Sleep', 'Clean', 'Exercise']
    >>> enumerate_tasks(tasks)
    ['0. Eat', '1. Sleep', '2. Clean']
    >>> enumerate_tasks(tasks, n=2)
    ['0. Eat', '1. Sleep']
    >>> enumerate_tasks(tasks, all_tasks=True)
    ['0. Eat', '1. Sleep', '2. Clean', '3. Exercise']
    >>> enumerate_tasks(tasks, from_beginning=False)
    ['3. Exercise', '2. Clean', '1. Sleep']
    >>> enumerate_tasks(tasks, n=10)
    ['0. Eat', '1. Sleep', '2. Clean', '3. Exercise']
    >>> enumerate_tasks(tasks, n=10, from_beginning=False)
    ['3. Exercise', '2. Clean', '1. Sleep', '0. Eat']
    '''

    if all_tasks:
        n = len(tasks)

    numbered_tasks = [f'{str(n)}. {line}' for n, line in enumerate(tasks)]

    if from_beginning:
        return numbered_tasks[:n]
    else:
        return numbered_tasks[-1:-n-1:-1]


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
    'The task list is empty!'
    '''

    try:
        return tasks[0]
    except IndexError as err:
        return 'The task list is empty!'


def pretty_print(list_of_strings, padding=2, outline='#'):
    length_of_longest_string = max([len(i) for i in list_of_strings])
    width = length_of_longest_string + 2 * (3*padding + 1)
    height = 1 + 2 * (padding + 1)
    top_bottom_string = outline * width
    padding_string = outline + ' ' * (width - 2) + outline
    pretty_list_of_strings = [outline + line.center(width-2) + outline for line in list_of_strings]
    lines = []
    lines.append(top_bottom_string)
    lines.extend([padding_string] * padding)
    lines.extend(pretty_list_of_strings)
    lines.extend([padding_string] * padding)
    lines.append(top_bottom_string)
    for line in lines:
        print(line)


def main():
    args = get_args()

    try:
        tasks = load_tasks(TODO_FILE)
    except FileNotFoundError:
        tasks = []

    if args.subparser_name == 'now':
        task = ' '.join(args.task)
        add_task_to_beginning(task, tasks)
        write_tasks(tasks, TODO_FILE)
    elif args.subparser_name == 'later':
        task = ' '.join(args.task)
        add_task_to_end(task, tasks)
        write_tasks(tasks, TODO_FILE)
    elif args.subparser_name == 'list':
        count = len(tasks)
        numbered_tasks = [f'{str(count)}. {line}' for count, line in enumerate(tasks)]
        tasks = list_tasks(numbered_tasks, n=args.task_count, all_tasks=args.all, from_beginning=not args.from_end)
        pretty_print(tasks)
    elif args.subparser_name == 'done':
        if args.interactive:
            pass
        else:
            deleted_task = delete_task(0, tasks)
            print(f'{deleted_task} is done!')
            write_tasks(tasks, TODO_FILE)
    else:
        pretty_print([current_task(tasks)])



if __name__ == '__main__':
    main()
