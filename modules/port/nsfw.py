#!/usr/bin/python3
"""
nsfw.py - some things just aren't safe for work, a casca module
author: Casey Link <unnamedrambler@gmail.com
"""

def nsfw(casca, input):
    """.nsfw <link> - Mark a link (or some text) as being not safe for work."""
    link = input.group(2)
    if not link:
        casca.say(".nsfw <link> - for when a link isn't safe for work")
        return
    casca.say("!!NSFW!! -> %s <- !!NSFW!!" % (link))
nsfw.rule = (['nsfw'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
