# Shellcut [![Build Status](https://travis-ci.org/radomirbosak/shellcut.svg?branch=master)](https://travis-ci.org/radomirbosak/shellcut)

_Shell shortcuts_

Automate your frequent commands by pasting a url/some string and performing a simple string replacement.

## Example

Shellcut installs a program called `s`. Calling
```
$ s https://github.com/kennethreitz/requests
```

will clone this repo to `/tmp/` and change the directory into it. The "magic" is performed with a config file like this:

```$ console
$ cat ~/.config/shellcut/my-shortcuts.yaml
---
shortcuts:
- name: Clone github repo
  match: https://github.com/{}/{}
  shell: |
    cd /tmp/
    git clone git@github.com:{}/{}.git
```

For more examples, navigate to [documentation](docs/usage.md).

## Installation
```
pip3 install . --user
```

## Testing
```console
make test
```

To continuously run tests (tests trigger on every file modification):
```console
make testloop
```

### Testing dependencies
_(some of these can be skipped)_
```console
pip3 install -r requirements.txt
dnf install colordiff
dnf install inotify-tools  # required for testloop Makefile goal
```
