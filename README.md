# Shellcut

_Shell shortcuts_

Automate your frequent commands by pasting a url/some string and performing a simple string replacement.

## Example

Let's call our program `s`. Calling
```
$ s https://github.com/kennethreitz/requests
```

will clone this repo to `/tmp/` and change the directory into it. The "magic" is performed with a config file like this:

```yaml
---
shortcuts:
- name: Clone github repo
  match: https://github.com/{}/{}
  shell: |
    cd /tmp/
    git clone git@github.com:{}/{}.git

```

## Installation
```
make install
```

### Installation Dependencies

```
dnf install python3-pyyaml
pip3 install parse xdg
```

## Testing
```
make test
```

### Testing dependencies
_(some of these can be skipped)_
```
dnf install colordiff inotify-tools
pip3 install green autopep8 flake8
```
