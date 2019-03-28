# todo.py

## Usage:

Link `todo.py` to somewhere in your `$PATH`:

    ln -s /path/to/todo.py ~/bin/todo

Run `todo -h`.

Profit!

## How it works

`todo.py` creates two lists. The first list contains things ordered from `now`, to `soon`. The second list contains things ordered from `later` to `maybe`.

### Default command

`todo` with no arguments lists the current task.

### Adding tasks

`todo now Task` adds `Task` to the beginning of the first list. `todo soon Task` adds `Task` to the end of the first list. `todo later` and `todo maybe` do the same thing with the second list.

Short versions of these commands are:

- `todo now`: `todo n`
- `todo soon`: `todo s`
- `todo later`: `todo l`
- `todo maybe`: `todo m`


### Listing tasks

`todo list` lists tasks with indexes. Optionally provide a count to list more than three tasks. See `todo list -h` for more options.

`todo list` has a short version: `todo ls`.

### Deleting tasks

`todo done` deletes the current task. Optionally provide a task index to delete tasks out of order. (Use `todo list` to determine task indexes.) See `todo done -h` for more options.

`todo done` does not have a short version, because it is a destructive operation.

### Structure of todo.yml file

These lists are stored in a `yaml` file with the following structure:

    - Eat
    - Sleep
    ---
    - Clean
    - Exercise

The default location of the yaml file is `~/.todo/todo.yml`. It is placed into a hidden directory, rather than as a hidden file in the home directory to allow the use of programs such as [Syncthing](https://syncthing.net/) to synchronise your tasks between computers and devices.