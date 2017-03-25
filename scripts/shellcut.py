#!/usr/bin/python3

import re
import os
import sys
import glob
import subprocess

import yaml
import parse

from xdg import XDG_CONFIG_HOME


def get_config_dir():
    """
    Return the config directory
    """
    if 'SHELLCUT_CONFIG' in os.environ:
        return os.environ['SHELLCUT_CONFIG']
    else:
        return os.path.join(XDG_CONFIG_HOME, 'shellcut.d')


def load_shortcuts(configdir):
    """
    Load shortcuts from the config directory
    """
    shortcuts = []
    for filename in glob.glob(os.path.join(configdir, '*.yaml')):
        y = yaml.load(open(filename))
        shortcuts.extend(y['shortcuts'])
    return shortcuts


def check_shortcuts(input_data, shortcuts, label=None, shell=None):
    """
    Returns the shortcuts matching input_data

    Returns: list of pairs (shortcut, script)
        shortcut: matched shortcut
        script: corresponding pattern script string
    """
    possible = []

    for shortcut in shortcuts:
        script = get_match(input_data, shortcut, label, shell)
        if script is not None:
            possible.append((shortcut, script))

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

    if not isinstance(pattern_label, list):
        pattern_label = [pattern_label]

    return cli_label in pattern_label


def get_match(input_data, shortcut, label=None, shell=None):
    """
    Check if 'input_data' matches the 'shortcut' pattern and if yes, return the
    substituted shell command.
    """

    # if the label does not match, return None
    if not label_matches(label, shortcut.get('label')):
        return

    # check if the pattern supports the given shell and default to 'shell'
    if shell in shortcut:
        script = shortcut[shell]
    elif 'shell' in shortcut:
        script = shortcut['shell']
    else:
        return None

    if 'match' in shortcut:
        conditions = shortcut['match']
        if not isinstance(conditions, list):
            conditions = [conditions]
        # check if any condition matches
        for condition in conditions:
            result = parse.parse(condition, input_data)
            if result is not None:
                return script.format(*result.fixed, **result.named)

    if 'regex' in shortcut:
        conditions = shortcut['regex']
        if not isinstance(conditions, list):
            conditions = [conditions]
        # check if any condition matches
        for condition in conditions:
            match = re.match(condition, input_data)
            if match:
                return script.format(*match.groups())
    return None


def get_active_shell():
    """
    Get the shell which the user is using

    Returns:
        'bash' or 'fish' or None
    """
    env_shell = os.environ['SHELL']
    for shell in ['bash', 'fish']:
        if env_shell.endswith(shell):
            return shell
    return None


def main():
    # load CLI arguments
    u = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) >= 3 else None

    env_shell = get_active_shell()

    # load and check shortcuts
    shortcuts = load_shortcuts(get_config_dir())
    possible_matches = check_shortcuts(u, shortcuts,
                                       label=label,
                                       shell=env_shell)

    # if the function returned no matches, exit
    if not possible_matches:
        print('Input matches none of the patterns')
        sys.exit(1)

    _, command_string = possible_matches[0]

    # print the string, which is later interpreted by bash/fish
    shell_cmd = env_shell if env_shell is not None else 'sh'
    subprocess.call([shell_cmd, "-c", command_string])


if __name__ == '__main__':
    main()
