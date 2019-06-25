#!/usr/bin/env python3
# coding: utf-8
"""
main.py
06-25-19
jack skrable
"""

import json
import collections

log_file = './data/20190624230312.json'

with open(log_file, encoding='utf8') as f:
    data = json.load(f)


def dig_logs(in_rec, errors=[], path=None):
    
    if type(in_rec) is dict:
        for key, val in in_rec.items():
            path = path + '.' + key if path else key
            if key == 'reason':
                # errors.append({path : val})
                errors.append(val)
            else:    
                dig_logs(val, errors, path)
    elif type(in_rec) is list:
    
        [dig_logs(x, errors, path) for x in in_rec]

    return errors

errors = dig_logs(data)
summary = collections.Counter(errors)

