#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
choose.py - sometimes you just can't decide, a casca module
"""

import re, random

def choose(casca, input):
    """.choose <red> <blue> - for when you just can't decide"""
    origterm = input.groups()[1]
    if not origterm:
        return casca.say(".choose <red> <blue> - for when you just can't decide")
    c = re.findall(r'([^,]+)', origterm)
    if len(c) == 1:
        c = re.findall(r'(\S+)', origterm)
        if len(c) == 1:
            return casca.reply("%s" % (c[0].strip()))
    fate = random.choice(c).strip()
    return casca.reply("%s" % (fate))
choose.rule = (['choose'], r'(.*)')

if __name__ == '__main__': 
    print(__doc__.strip())
