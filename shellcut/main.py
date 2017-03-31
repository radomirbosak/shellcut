#!/usr/bin/python3

import re
import os
import sys
import glob
import argparse
import subprocess

import yaml
import parse

try:
    from xdg import XDG_CONFIG_HOME
except ImportError:
    XDG_CONFIG_HOME = '~/.config'


AVAILABLE_EXECUTORS = ['bash', 'fish', 'python']


def get_config_dirs():
    """
    Return the list of directories to search configs in
    """
    config_dirs = list()

    # search the directory determined by SHELLCUT_CONFIG env var
    if 'SHELLCUT_CONFIG' in os.environ:
        config_dirs.append(os.environ['SHELLCUT_CONFIG'])

    # search config/ in the current module
    current_dir = os.path.dirname(__file__)
    config_dirs.append(
        os.path.join(current_dir, 'config'))

    # search ~/.config
    config_dirs.append(
        os.path.join(XDG_CONFIG_HOME, 'shellcut'))
    return config_dirs


def load_shortcuts(configdirs):
    """
    Load shortcuts from the config directory
    """
    shortcuts = []
    for configdir in configdirs:
        for filename in glob.glob(os.path.join(configdir, '*.yaml')):
            y = yaml.load(open(filename))
            shortcuts.extend(y['shortcuts'])
    return shortcuts


def check_shortcuts(input_data, shortcuts, label=None):
    """
    Returns the shortcuts matching input_data

    Returns: list of pairs (shortcut, script)
        shortcut: matched shortcut
        script: corresponding pattern script string
    """
    possible = []

    for shortcut in shortcuts:
        executor_map = get_match(input_data, shortcut, label)
        # check if the pattern supports the given shell and default to 'shell'

        if executor_map:
            possible.append((shortcut, executor_map))

    return possible


def label_matches(cli_label, pattern_label):
    """
    Checks if the label provided via CLI matches the label (or list of labels)
    from the pattern

    Returns:
        True if label matches, otherwise False
    """
    if not cli_label:
        return True

    return cli_label in listify(pattern_label)


def get_match(input_data, shortcut, label=None):
    """
    Check if 'input_data' matches the 'shortcut' pattern and if yes, return the
    substituted shell command.
    """

    # if the label does not match, return None
    if not label_matches(label, shortcut.get('label')):
        return

    executor_map = {}

    conditions_match = listify(shortcut.get('match', []))
    conditions_regex = listify(shortcut.get('regex', []))

    # fetch executors from match-type patterns
    for condition in conditions_match:
        result = parse.parse(condition, input_data)
        if result is None:
            continue
        executor_map.update({
            executor: shortcut[executor].format(
                *result.fixed, **result.named)
            for executor in AVAILABLE_EXECUTORS
            if executor in shortcut
        })

    # fetch executors from regex-type patterns
    for condition in conditions_regex:
        match = re.match(condition, input_data)
        if not match:
            continue
        executor_map.update({
            executor: shortcut[executor].format(*match.groups())
            for executor in AVAILABLE_EXECUTORS
            if executor in shortcut
        })

    return executor_map or None


def get_input(text):
    """
    Wrapper for python's input builtin
    """
    return input(text)


def choose_match(possible_matches):
    """
    Promt user to choose from multiple matching patterns
    """
    print('Choose one:')
    for i, (shortcut, match) in enumerate(possible_matches):
        print('{}: {}'.format(i + 1, shortcut['name']))
    answer = int(get_input('> '))
    print(answer)

    if 1 <= answer <= len(possible_matches):
        return possible_matches[answer - 1][1]
    else:
        raise ValueError('Invalid choice')


def parse_arguments():
    """
    Parse CLI arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('label', nargs='?')

    return parser.parse_args()


def choose_single_match(possible_matches):
    """
    Get the list of possible matches and decide for the correct one

    Returns:
        command_string: the command to run
    """
    if not possible_matches:
        print('Input matches none of the patterns')
        sys.exit(1)

    if len(possible_matches) > 1:
        try:
            command_string = choose_match(possible_matches)
        except ValueError:
            print('Invalid choice')
            sys.exit(1)
        except KeyboardInterrupt:
            print('Program Interrupted')
            sys.exit(1)
    else:
        _, command_string = possible_matches[0]

    return command_string


def listify(element):
    """
    Returns the argument if it's a list, otherwise a new list containing only
    this one element.
    """
    return element if isinstance(element, list) else [element]


def main():
    # load CLI arguments
    args = parse_arguments()

    # load and check shortcuts
    shortcuts = load_shortcuts(get_config_dirs())
    possible_matches = check_shortcuts(args.input, shortcuts,
                                       label=args.label)

    # if the function returned no matches, exit
    executor_map = choose_single_match(possible_matches)

    # run all executors
    for command, script in executor_map.items():
        subprocess.call([command, "-c", script])


if __name__ == '__main__':
    main()
