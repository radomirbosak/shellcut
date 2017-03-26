# Usage
## Matching syntax

_shellcut_ uses two syntaxes to define a pattern:
* python regex syntax _(keyword: regex)_
* python format syntax _(keyword: match)_

The two patterns in following example config file match the same inputs:
```yaml
---
shortcuts:
- name: Describe person
  match: Hello, my name is {} and I am {} years old
  shell: |
    echo Name: {}
    echo Age: {}

- name: Describe person
  regex: Hello, my name is (.*?) and I am (.*?) years old
  shell: |
    echo Name: {}
    echo Age: {}
```

You can refer to match groups by their name and position:
```yaml
---
shortcuts:
- name: Describe person
  match: Hello, my name is {}, I like {likes} and I am {} years old
  shell: |
    echo Age: {1}
    echo Name: {0}
    echo Likes: {likes}
```

## Labels and multiple matching patterns

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
_shellcut_ prompts you to choose the right action:
```console
$ s bashrc
Choose one:
1: Edit .bashrc
2: Backup .bashrc
> 2
2
.bashrc backed up to /tmp
```

You can make the choice clear upfront by specifying a label:
```console
$ s bashrc backup
Choose one:
1: Edit .bashrc
2: Backup .bashrc
> 2
2
.bashrc backed up to /tmp
```

## Configuration files

_shellcut_ loads shortcut patterns from _.yaml_ files which it searches for in all of the following directories:
* `~/.config/`
* `$SHELLCUT_CONFIG/`  _(if the environment variable is set)_
* `<shellcut_module_installation_path>/config`

Config files must have the yaml syntax and can be of this form:

```yaml
---
shortcuts:
- name: Pattern name
  match: Format-type match pattern
  regex: Regex-type match pattern
  shell: |
    echo "These commands are executed"
    echo "When the command input matches one of the patterns"
  label:
  - LABEL1
  - LABEL2
```

The "label" key can either contain a string or a list of strings.
