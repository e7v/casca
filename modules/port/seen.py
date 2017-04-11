#!/usr/bin/env python
"""
seen.py - casca Seen Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/
"""

import time

## TODO: Make it save .db to disk

def f_seen(casca, input):
    """.seen <nick> - Reports when <nick> was last seen."""

    if not input.group(2):
        return casca.say('Please provide a nick.')
    nick = input.group(2).lower()

    if not hasattr(casca, 'seen'):
        return casca.reply('?')

    if casca.seen.has_key(nick):
        channel, t = casca.seen[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))
        msg = 'I last saw %s at %s in some channel.' % (nick, t)
        casca.say(msg)
    else:
        casca.say("Sorry, I haven't seen %s around." % nick)
f_seen.rule = r'(?i)^\.(seen)\s+(\w+)'
f_seen.rate = 15

def f_note(casca, input):
    try:
        if not hasattr(casca, 'seen'):
            casca.seen = dict()
        if input.sender.startswith('#'):
            casca.seen[input.nick.lower()] = (input.sender, time.time())
    except Exception, e: print e
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
