# Shellcut

_Shell shortcuts_

Automate your frequent commands by pasting a url/some string and performing a simple string replacement.

## Example

Let's call your program `u`. Calling
```
$ u https://github.com/kennethreitz/requests
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
