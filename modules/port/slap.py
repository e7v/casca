#!/usr/bin/env python
"""
scores.py - casca Slap Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/casca/
"""

import random

def slap(casca, input):
    """.slap <target> - Slaps <target>"""
    text = input.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1] == casca.nick:
        if (input.nick not in casca.config.admins):
            text[1] = input.nick
        else: text[1] = 'herself'
    if text[1] in casca.config.admins:
        if (input.nick not in casca.config.admins):
            text[1] = input.nick
    verb = random.choice(('slaps', 'kicks', 'destroys', 'annihilates', 'obliterates', 'drop kicks', 'curb stomps', 'backhands', 'punches', 'roundhouse kicks', 'rusty hooks', 'pwns', 'owns'))
    casca.write(['PRIVMSG', input.sender, ' :\x01ACTION', verb, text[1], '\x01'])
slap.commands = ['slap', 'slaps']
slap.priority = 'medium'
slap.rate = 60

if __name__ == '__main__':
    print __doc__.strip()
