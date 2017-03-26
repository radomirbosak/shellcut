# Shellcut [![Build Status](https://travis-ci.org/radomirbosak/shellcut.svg?branch=master)](https://travis-ci.org/radomirbosak/shellcut)

_Shell shortcuts_

Automate your frequent commands by pasting a url/some string and performing a simple string replacement.

## Example

Shellcut installs a program called `s`. Calling
```
$ s https://github.com/kennethreitz/requests
```

will clone this repo to `/tmp/` and change the directory into it. The "magic" is performed with a config file like this:

```console
$ cat ~/.config/shellcut/default.yaml
```
```yaml
---
shortcuts:
- name: Clone github repo
  match: https://github.com/{}/{}
  shell: |
    cd /tmp/
    git clone git@github.com:{}/{}.git

```

Or maybe you just want to define some aliases, but not mess with the global program namespace?

If there are multiple patterns matching the input, e.g. from a config file like this:
```yaml
---
shortcuts:
- name: Edit .bashrc
  regex: ^bashrc$
  shell: vim ~/.bashrc
  label: edit

- name: Backup .bashrc
  regex: ^bashrc$
  shell: |
    mkdir -p /tmp/backup
    cp ~/.bashrc /tmp/backup
    echo ".bashrc backed up to /tmp"
  label: backup
```
_shellcut_ prompt you to choose the right action:
```console
$ s bashrc
Choose one:
1: Edit .bashrc
2: Backup .bashrc
> 2
2
.bashrc backed up to /tmp
```

You can make it clear by specifying a label:
```console
$ s bashrc backup
Choose one:
1: Edit .bashrc
2: Backup .bashrc
> 2
2
.bashrc backed up to /tmp
```

## Installation
```
pip3 install . --user
```

## Testing
```console
make test
```
or
```console
tox
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
