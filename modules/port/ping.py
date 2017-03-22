#!/usr/bin/env python
"""
ping.py - casca Ping Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)

More info:
 * casca: https://github.com/myano/casca/
 * Phenny: http://inamidst.com/casca/
"""

import random


def interjection(casca, input):
    """response to interjections"""
    casca.say(input.nick + '!')
interjection.rule = r'($nickname!)'
interjection.priority = 'high'
interjection.example = '$nickname!'


def f_ping(casca, input):
    """ping casca in a channel or pm"""
    casca.reply('pong!')
f_ping.rule = r'(?i)$nickname[:,]?\sping'
f_ping.priority = 'high'
f_ping.example = '$nickname: ping!'

if __name__ == '__main__':
    print __doc__.strip()
