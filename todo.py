#!/usr/bin/env python3

# todo.py

# Create and manage an ordered list of tasks.
# Tasks may be added either to the start or the end of the list.
# Tasks are stored in yaml format.

from pathlib import Path
from yaml import safe_load_all, safe_dump_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


TODO_FILE = Path('~/.todo/todo.yml').expanduser()
Path.mkdir(TODO_FILE.parent, exist_ok=True)


def get_args():
    import argparse

    # create top level parser
    parser = argparse.ArgumentParser(description='Manage a todo list.')
    parser.add_argument('--ugly', '-u', action='store_true', help='No pretty printing!')
    subparsers = parser.add_subparsers(dest='subparser_name', help='View help for sub-commands with "%(prog)s command -h"')

    # create parser for the 'now' command
    parser_now = subparsers.add_parser('now', aliases=['n'], help='Add task to do now')
    parser_now.add_argument('task', type=str, nargs='+', help='Task to add.') 

    # create parser for the 'soon' command
    parser_soon = subparsers.add_parser('soon', aliases=['s'], help='Add task to do soon')
    parser_soon.add_argument('task', type=str, nargs='+', help='Task to add.') 

    # create parser for the 'later' command
    parser_later = subparsers.add_parser('later', aliases=['l'], help='Add task to do later')
    parser_later.add_argument('task', type=str, nargs='+', help='Task to add.')

    # create parser for the 'maybe' command
    parser_maybe = subparsers.add_parser('maybe', aliases=['m'], help='Add task to do maybe')
    parser_maybe.add_argument('task', type=str, nargs='+', help='Task to add.') 

    # create parser for the 'list' command
    parser_list = subparsers.add_parser('list', aliases=['ls'], help='List tasks')
    parser_list.add_argument('--all', '-a', action='store_true', help='List all tasks')
    parser_list.add_argument('--from-end', '-e', action='store_true', help='List tasks in reverse order (beginning with lowest priority)')
    parser_list.add_argument('task_count', metavar='N', default=3, nargs='?', type=int, help='Number of tasks to list')

    # create parser for the 'done' command
    parser_done = subparsers.add_parser('done', help='Complete task (defaults to current task)')
    parser_done.add_argument('task_index', metavar='index', type=int, nargs='?', default=0, help='Index of task to delete. (Use `list` subcommand to determine index).')
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
    >>> tasks = [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    >>> write_tasks(tasks, todo_file)
    >>> load_tasks(todo_file)
    [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    '''

    with open(todo_file, 'w') as file:
        safe_dump_all(tasks, file, default_flow_style=False)


def load_tasks(todo_file):
    '''Load tasks from file.

    >>> todo_file = Path('./test_todo.yml')
    >>> load_tasks(todo_file)
    [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    '''

    with open(todo_file, 'r') as file:
        # If we return the generator here, we close the file before we read it!
        return list(safe_load_all(file))


def add_task_to_now(task, task_lists):
    '''Add task to beginning of now list, to do now.

    >>> task_lists = [['Eat', 'Sleep'], []]
    >>> task = 'Clean'
    >>> add_task_to_now(task, task_lists)
    >>> task_lists
    [['Clean', 'Eat', 'Sleep'], []]
    '''

    task_lists[0].insert(0, task)


def add_task_to_soon(task, task_lists):
    '''Add task to end of now list, to do soon.

    >>> task_lists = [['Eat', 'Sleep'], []]
    >>> task = 'Clean'
    >>> add_task_to_soon(task, task_lists)
    >>> task_lists
    [['Eat', 'Sleep', 'Clean'], []]
    '''

    task_lists[0].append(task)


def add_task_to_later(task, task_lists):
    '''Add task to beginning of later list, to do later.

    >>> task_lists = [['Eat', 'Sleep'], ['Clean']]
    >>> task = 'Exercise'
    >>> add_task_to_later(task, task_lists)
    >>> task_lists
    [['Eat', 'Sleep'], ['Exercise', 'Clean']]
    '''

    task_lists[1].insert(0, task)


def add_task_to_maybe(task, task_lists):
    '''Add task to end of later list, to do maybe.

    >>> task_lists = [['Eat', 'Sleep'], ['Clean']]
    >>> task = 'Exercise'
    >>> add_task_to_maybe(task, task_lists)
    >>> task_lists
    [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    '''

    task_lists[1].append(task)


def delete_task(task_index, task_lists):
    '''Delete and return task with specified index (index begins at 0)

    >>> task_lists = [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    >>> delete_task(0, task_lists)
    'Eat'
    >>> task_lists == [['Sleep'], ['Clean', 'Exercise']]
    True
    >>> task_lists = [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    >>> delete_task(2, task_lists)
    'Clean'
    >>> task_lists == [['Eat', 'Sleep'], ['Exercise']]
    True
    >>> task_lists = [['Eat', 'Sleep'], ['Clean', 'Exercise']]
    >>> delete_task(3, task_lists)
    'Exercise'
    >>> task_lists == [['Eat', 'Sleep'], ['Clean']]
    True
    >>> task_lists = [['Eat', 'Sleep'], ['Clean', 'Exercise'], ['Write', 'Edit']]
    >>> delete_task(4, task_lists)
    'Write'
    >>> task_lists == [['Eat', 'Sleep'], ['Clean', 'Exercise'], ['Edit']]
    True
    '''

    list_index = 0
    for task_list in task_lists:
        if task_index > len(task_list) - 1:
            list_index += 1
            task_index -= len(task_list)
        else:
            break
    return task_lists[list_index].pop(task_index)


# This code isn't currently used...
#def enumerate_tasks(tasks, n=3, all_tasks=False, from_beginning=True):
#    '''Number and list n tasks. Defaults to n=3, starting from the most current task
#
#    >>> tasks = ['Eat', 'Sleep', 'Clean', 'Exercise']
#    >>> enumerate_tasks(tasks)
#    ['0. Eat', '1. Sleep', '2. Clean']
#    >>> enumerate_tasks(tasks, n=2)
#    ['0. Eat', '1. Sleep']
#    >>> enumerate_tasks(tasks, all_tasks=True)
#    ['0. Eat', '1. Sleep', '2. Clean', '3. Exercise']
#    >>> enumerate_tasks(tasks, from_beginning=False)
#    ['3. Exercise', '2. Clean', '1. Sleep']
#    >>> enumerate_tasks(tasks, n=10)
#    ['0. Eat', '1. Sleep', '2. Clean', '3. Exercise']
#    >>> enumerate_tasks(tasks, n=10, from_beginning=False)
#    ['3. Exercise', '2. Clean', '1. Sleep', '0. Eat']
#    '''
#
#    if all_tasks:
#        n = len(tasks)
#
#    numbered_tasks = [f'{str(n)}. {line}' for n, line in enumerate(tasks)]
#
#    if from_beginning:
#        return numbered_tasks[:n]
#    else:
#        return numbered_tasks[-1:-n-1:-1]


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


def flatten(list_of_lists):
    '''Flatten list of lists into single list

    >>> list_of_lists = [[1, 2, 3], [4, 5, 6]]
    >>> flatten(list_of_lists)
    [1, 2, 3, 4, 5, 6]
    >>> list_of_lists = [[1, [2, [3]]], [4, 5, 6]]
    >>> flatten(list_of_lists)
    [1, 2, 3, 4, 5, 6]
    '''

    flat_list = []
    for item in list_of_lists:
        if type(item) == list:
            item = flatten(item)
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return flat_list


def pretty_print(list_of_strings, padding=2, outline='#'):
    try:
        length_of_longest_string = max([len(i) for i in list_of_strings])
    except ValueError:
        length_of_longest_string = 0
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

def ugly_print(list_of_strings):
    for line in list_of_strings:
        print(line)


def main():
    args = get_args()
    if args.ugly:
        print_out = ugly_print
    else:
        print_out = pretty_print

    try:
        task_lists = load_tasks(TODO_FILE)
    except FileNotFoundError:
        task_lists = [[],[]]

    if args.subparser_name in ['now', 'n']:
        task = ' '.join(args.task)
        add_task_to_now(task, task_lists)
        write_tasks(task_lists, TODO_FILE)
    elif args.subparser_name in ['soon', 's']:
        task = ' '.join(args.task)
        add_task_to_soon(task, task_lists)
        write_tasks(task_lists, TODO_FILE)
    elif args.subparser_name in ['later', 'l']:
        task = ' '.join(args.task)
        add_task_to_later(task, task_lists)
        write_tasks(task_lists, TODO_FILE)
    elif args.subparser_name in ['maybe', 'm']:
        task = ' '.join(args.task)
        add_task_to_maybe(task, task_lists)
        write_tasks(task_lists, TODO_FILE)
    elif args.subparser_name in ['list', 'ls']:
        merged_task_lists = flatten(task_lists)
        count = len(merged_task_lists)
        numbered_tasks = [f'{str(count)}. {line}' for count, line in enumerate(merged_task_lists)]
        task_list = list_tasks(numbered_tasks, n=args.task_count, all_tasks=args.all, from_beginning=not args.from_end)
        if len(task_list) > 0:
            print_out(task_list)
        else:
            print_out(['The task list is empty!'])
    elif args.subparser_name == 'done':
        if args.interactive:
            print('This option is not implemented yet')
        else:
            deleted_task = delete_task(args.task_index, task_lists)
            print(f'{deleted_task} is done!')
            write_tasks(task_lists, TODO_FILE)
    else:
        print_out([current_task(flatten(task_lists))])



if __name__ == '__main__':
    main()
