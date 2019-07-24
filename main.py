#!/usr/bin/env python3
# coding: utf-8
"""
main.py
06-25-19
jack skrable
"""

import json
import collections
import sys
import string
import argparse


# Progress bar for cli
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def arg_parser():
    # function to parse arguments sent to CLI
    # setup argument parsing with description and -h method
    parser = argparse.ArgumentParser(
        description='Summarizes logs from a json file')
    parser.add_argument('-f', '--file', default='./datasets/sample.json', type=str, nargs='?',
                        help='path of the file to summarize')
    # parse args and return
    args = parser.parse_args()
    return args




def dig_logs(in_rec, errors=[], path=None):
    
    if type(in_rec) is dict:
        for key, val in in_rec.items():
            # path = path + '.' + key if path else key
            if key == 'reason':
                # errors.append({'path': path, 'error' : val})
                errors.append(val)
            elif type(val) is dict or list:
                path = path + '.' + key if path else key    
                dig_logs(val, errors, path)
    elif type(in_rec) is list:
        [dig_logs(x, errors, path) for x in in_rec]
    return errors


# MAIN
#####################################################################
args = arg_parser()
INFILE = args.file

# log_file = './data/load_errors.json'

with open(INFILE, encoding='utf8') as f:
    data = json.load(f)

errors = dig_logs(data)
summary = dict(collections.Counter(errors))

print('Error Message    :   Count')
print(summary)

