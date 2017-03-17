#!/usr/bin/python3

import re
import os
import sys
import glob
import yaml

import parse


HOME = os.environ['HOME']
configdir = os.path.join(HOME, '.config', 'shellcut.d')


def load_shortcuts():
    """
    Load shortcuts from the ~/.config/shellcut.d/directory
    """
    shortcuts = []
    for filename in glob.glob(os.path.join(configdir, '*.yaml')):
        y = yaml.load(open(filename))
        shortcuts.extend(y['shortcuts'])
    return shortcuts


def check_shortcuts(input_data, shortcuts):
    """
    Check for each every shortcut if the input string matches it
    """
    for cut in shortcuts:
        if 'match' in cut:
            result = parse.parse(cut['match'], input_data)
            if result is not None:
                print(cut['shell'].format(*result.fixed, **result.named))
                break
        if 'regex' in cut:
            match = re.match(cut['regex'], input_data)
            if match:
                print(cut['shell'].format(*match.groups()))
                break
    else:
        sys.exit(1)

    sys.exit(0)


def main():
    u = sys.argv[1]
    shortcuts = load_shortcuts()
    check_shortcuts(u, shortcuts)


if __name__ == '__main__':
    main()
