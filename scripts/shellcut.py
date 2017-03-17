#!/usr/bin/python3

import re
import os
import sys
import glob
import yaml

import parse

from xdg import XDG_CONFIG_HOME

configdir = os.path.join(XDG_CONFIG_HOME, 'shellcut.d')


def load_shortcuts():
    """
    Load shortcuts from the ~/.config/shellcut.d/directory
    """
    shortcuts = []
    for filename in glob.glob(os.path.join(configdir, '*.yaml')):
        y = yaml.load(open(filename))
        shortcuts.extend(y['shortcuts'])
    return shortcuts


def check_shortcuts(input_data, shortcuts, label=None):
    """
    Check for each every shortcut if the input string matches it

    Returns: replaced string
    """
    possible = []

    for cut in shortcuts:
        match = get_match(input_data, cut, label)
        if match is not None:
            possible.append(match)

    if not possible:
        return None

    return possible[0]


def get_match(input_data, shortcut, label=None):
    """
    Check if 'input_data' matches the 'shortcut' pattern and if yes, return the
    substituted shell command.
    """
    if label and shortcut.get('label') != label:
        return None

    if 'match' in shortcut:
        result = parse.parse(shortcut['match'], input_data)
        if result is not None:
            return shortcut['shell'].format(*result.fixed, **result.named)

    if 'regex' in shortcut:
        match = re.match(shortcut['regex'], input_data)
        if match:
            return shortcut['shell'].format(*match.groups())
    return None


def main():
    # load CLI arguments
    u = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) >= 3 else None

    # load and check shortcuts
    shortcuts = load_shortcuts()
    command_string = check_shortcuts(u, shortcuts, label=label)

    # if the function returned None, we have no match
    if command_string is None:
        sys.exit(1)

    # print the string, which is later interpreted by bash/fish
    print(command_string)


if __name__ == '__main__':
    main()
