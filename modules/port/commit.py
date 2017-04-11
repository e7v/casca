#!/usr/bin/python3
"""
commit.py - what the commit
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import web
#from tools import GrumbleError


def commit(casca, input):
    """.commit - Get a What the Commit commit message."""

    try:
        msg = web.get("http://whatthecommit.com/index.txt")
    except: pass
    casca.reply(msg)
commit.commands = ['commit']

if __name__ == '__main__':
    print(__doc__.strip())
