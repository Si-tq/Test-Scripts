#!/usr/bin/python3

import argparse
import hashlib
import json
import sys
from datetime import datetime


def parse_args(parser, commands):
    # Divide argv by commands
    split_argv = [[]]
    for c in sys.argv[1:]:
        if c in commands.choices:
            split_argv.append([c])
        else:
            split_argv[-1].append(c)
    # Initialize namespace
    args = argparse.Namespace()
    for c in commands.choices:
        setattr(args, c, None)
    # Parse each command
    parser.parse_args(split_argv[0], namespace=args)  # Without command
    for argv in split_argv[1:]:  # Commands
        n = argparse.Namespace()
        setattr(args, argv[0], n)
        parser.parse_args(argv, namespace=n)
    return args


parser = argparse.ArgumentParser()
commands = parser.add_subparsers(title='commands')

# Add Command
add_parser = commands.add_parser('add')
add_parser.add_argument('--name')
add_parser.add_argument('--deadline', help='"2011-11-04T00:05:23" Example date')
add_parser.add_argument('--description')

# Update Command
update_parser = commands.add_parser('update')
update_parser.add_argument('--name')
update_parser.add_argument('--deadline', help='"2011-11-04T00:05:23" Example date')
update_parser.add_argument('--description')
update_parser.add_argument('task_hash')

# Remove Command
remove_parser = commands.add_parser('remove')
remove_parser.add_argument('task_hash')

# List Command
list_parser = commands.add_parser('list')
list_parser.add_argument('--all', action='store_true')
list_parser.add_argument('--today', action='store_true')

try:
    with open('tasks.json', 'r+') as f:
        data = json.load(f)
except:
    data = list()

args = parse_args(parser, commands)


def tasks_add(name, deadline, description):
    """
    Method to return dict from ADD command arguments
    """
    _dict = {
        'name': name,
        'deadline': datetime.fromisoformat(deadline).__str__(),
        'description': description,
    }
    _dict['task_hash'] = hashlib.sha1(repr(sorted(_dict.items())).encode('utf-8')).hexdigest()
    return _dict


def tasks_update(name, deadline, description, task_hash):
    """
    Method to return dict from UPDATE command arguments
    """
    return {
        'name': name,
        'deadline': datetime.fromisoformat(deadline).__str__(),
        'description': description,
        'task_hash': task_hash
    }


def tasks_remove(task_hash):
    """
    Method to return variable from REMOVE command arguments
    """
    return task_hash


def tasks_list_all(data):
    """
    Method to return list of all records.
    """
    return [print(x) for x in data]


def tasks_list_today(data):
    """
    Method to return list of all records that deadline is in present day.
    """

    today_tasks = list()
    for x in data:
        date = datetime.fromisoformat(x.get('deadline'))
        if datetime.now().day == date.day and datetime.now().month == date.month and datetime.now().year == date.year:
            today_tasks.append(x)
    return [print(task) for task in today_tasks]


## BELOW Working commands logic with saving file in .json

# add logic
if args.add:
    task_hash = tasks_add(**vars(args.add)).get('task_hash')
    if data:
        for item in data:
            if task_hash not in [x.get('task_hash') for x in data]:
                data.append(tasks_add(**vars(args.add)))
                print('Added task!')
    else:
        data.append(tasks_add(**vars(args.add)))
        print('Added your first task!')

# update logic
if args.update:
    input_data = tasks_update(**vars(args.update))
    task_hash = input_data.get('task_hash')
    if data:
        if task_hash in [x.get('task_hash') for x in data]:
            for item in data:
                if task_hash == item.get('task_hash'):
                    item['name'] = input_data.get('name')
                    item['deadline'] = input_data.get('deadline')
                    item['description'] = input_data.get('description')
                    print('Update success!')
                    break
                else:
                    continue
        else:
            print('Task you looking for does not exist.')
    else:
        print('The database is currently empty.')

# removal logic
if args.remove:
    task_hash = tasks_remove(args.remove.task_hash)
    if data:
        if task_hash in [x.get('task_hash') for x in data]:
            for item in data:
                if task_hash == item.get('task_hash'):
                    data.remove(item)
                    print('Removal success!')
                    break
                else:
                    continue
        else:
            print('Task you looking for does not exist.')
    else:
        print('The database is currently empty.')

# listing logic
if args.list:
    if args.list.all:
        tasks_list_all(data)
    elif args.list.today:
        tasks_list_today(data)
    else:
        parser.parse_args(['-h'])

# Save .json file
with open('tasks.json', 'w+') as f:
    json.dump(data, f, indent=2)
