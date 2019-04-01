# todo.py

## Examples

	$ todo
	#################
	#               #
	#               #
	#      Eat      #
	#               #
	#               #
	#################
	$ todo ls
	######################
	#                    #
	#                    #
	#       0. Eat       #
	#      1. Sleep      #
	#      2. Clean      #
	#                    #
	#                    #
	######################
	$ todo now Install todo.py
	$ todo ls
	################################
	#                              #
	#                              #
	#      0. Install todo.py      #
	#            1. Eat            #
	#           2. Sleep           #
	#                              #
	#                              #
	################################
	$ todo ls -a
	################################
	#                              #
	#                              #
	#      0. Install todo.py      #
	#            1. Eat            #
	#           2. Sleep           #
	#           3. Clean           #
	#         4. Exercise          #
	#                              #
	#                              #
	################################
	$ todo done
	Install todo.py is done!
	$ todo ls
	######################
	#                    #
	#                    #
	#       0. Eat       #
	#      1. Sleep      #
	#      2. Clean      #
	#                    #
	#                    #
	######################

## Install

Clone this repository:

    git clone https://github.com/daviewales/todo.py.git
    
Navigate to `todo.py`:

    cd todo.py

Install dependencies (PyYaml):

    pip3 install -r requirements.txt

Link `todo.py` to somewhere in your `$PATH`:

    ln -s /path/to/todo.py ~/bin/todo

Run `todo -h`.

Profit!

## Usage

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

### TODO_PATH Environment variable

`todo.py` supports the environment variable `TODO_PATH`. The value of `TODO_PATH` must be a path to a directory.
For example the following will create a todo list in the Desktop folder, and add 'Sleep' as the current task:

    TODO_PATH="~/Desktop" todo now Sleep

This may be useful if you need to store your `todo.py` file in a different directory to the default, such as when running in Termux on Android.

### Ugly mode

By default, `todo.py` outputs tasks enclosed by a border of '#' symbols.
Passing the command-line argument `--ugly` or `-u` will display the tasks in a more straightforward manner.

### Running in Termux on Android

`todo.py` should work find in Termux.
However, there are a number of tweaks that you may wish to use.

You will need to edit the following file:

    /data/data/com.termux/file/usr/etc/bash.bashrc

Add the following lines:

    export TODO_PATH="~/storage/shared/todo"
    alias todo="todo -u"

This assumes that you have linked `todo.py` to somewhere in your path, using `todo` as the name of the link.

This will change the default directory to one which is writable by Termux.
It will also use 'Ugly mode' for outputting tasks, which works better on a small display.

### Testing

Run doctests (Use `-v` flag for more info):

    python3 -m doctest todo.py
    
OR

    nosetests --with-doctest todo.py
