#!/usr/bin/python3

import os
import sys
import yaml
import parse


HOME = os.environ['HOME']
filename = os.path.join(HOME, '.config', 'shellcut.yaml')


y = yaml.load(open(filename))

u = sys.argv[1]

for cut in y['shortcuts']:
    result = parse.parse(cut['regex'], u)
    if result is not None:
        print(cut['shell'].format(*result.fixed, **result.named))
        break
else:
    sys.exit(1)

sys.exit(0)
