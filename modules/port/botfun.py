#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

otherbot = "quone"

def botfight(casca, input):
    """.botfight - Fight the other bot in the channel."""

    messages = ["hits %s", "punches %s", "kicks %s", "hits %s with a rubber hose", "stabs %s with a clean kitchen knife"]
    response = random.choice(messages)

    casca.do(response % otherbot)
botfight.commands = ['botfight']
botfight.priority = 'low'
botfight.example = '.botfight'

def bothug(casca, input):
    """.bothug - Hug the other bot in the channel."""

    casca.do("hugs %s" % otherbot)
bothug.commands = ['bothug']
bothug.priority = 'low'
bothug.example = '.bothug'

if __name__ == '__main__':
    print(__doc__.strip())
