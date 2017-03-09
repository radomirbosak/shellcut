#!/usr/bin/python3

import os
import sys
import glob
import yaml

import parse


HOME = os.environ['HOME']
configdir = os.path.join(HOME, '.config', 'shellcut.d')


shortcuts = []
for filename in glob.glob(os.path.join(configdir, '*.yaml')):
    y = yaml.load(open(filename))
    shortcuts.extend(y['shortcuts'])

u = sys.argv[1]

for cut in shortcuts:
    result = parse.parse(cut['regex'], u)
    if result is not None:
        print(cut['shell'].format(*result.fixed, **result.named))
        break
else:
    sys.exit(1)

sys.exit(0)
