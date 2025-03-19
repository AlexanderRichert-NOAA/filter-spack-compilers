#!/usr/bin/env python3

import argparse
import os
import sys
from ruamel.yaml import YAML

parser = argparse.ArgumentParser(
  prog='filter_spack_compilers.py',
  description='Inclusively or exclusively delete compilers from compilers.yaml or spack.yaml.',
  epilog='Written by Alex Richert, March 2025',
)
parser.add_argument('yamlfile', help='Input YAML file (compilers.yaml or spack.yaml)')
parser.add_argument('compilerspecs', nargs='+', help='Compiler specs to keep/remove')
inc_or_exc_group = parser.add_mutually_exclusive_group(required=True)
inc_or_exc_group.add_argument('--remove', action='store_true')
inc_or_exc_group.add_argument('--keep-only', action='store_true')
args = parser.parse_args()

yaml = YAML(typ='rt')
yaml.default_flow_style = False
with open(args.yamlfile, 'r') as file:
  raw_yaml_data = yaml.load(file)

if 'spack' in raw_yaml_data.keys():
  yaml_data = raw_yaml_data['spack']
else:
  yaml_data = raw_yaml_data

n_compilers = len(yaml_data['compilers'])
for i in range(n_compilers-1,-1,-1):
  if (yaml_data['compilers'][i]['compiler']['spec'] in args.compilerspecs) and args.remove:
    del(yaml_data['compilers'][i])
    continue
  if (yaml_data['compilers'][i]['compiler']['spec'] not in args.compilerspecs) and args.keep_only:
    del(yaml_data['compilers'][i])

if 'spack' in raw_yaml_data.keys():
  raw_yaml_data['spack'] = yaml_data
  yaml_data = raw_yaml_data

bkp_path = args.yamlfile + '.bkp'
os.rename(args.yamlfile, bkp_path)

with open(args.yamlfile, 'w') as outputfile:
  yaml.dump(yaml_data, outputfile)
