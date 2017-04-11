#!/usr/bin/env python
"""
hugs.py - casca Hugs Module
Copyright 2015, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/
"""


def hugs(casca, input):
    '''.hugs <nick> -- have casca hug somebody'''
    txt = input.group(2)
    if not txt:
        msg = '\x01ACTION hugs %s\x01' % (input.nick)
        return casca.msg(input.sender, msg, x=True)
    parts = txt.split()
    to = parts[0]
    if to == casca.config.nick:
        to = 'themself'

    msg = '\x01ACTION hugs %s\x01' % (to)
    casca.msg(input.sender, msg, x=True)
hugs.commands = ['hug', 'hugs']

if __name__ == '__main__':
    print __doc__.strip()
