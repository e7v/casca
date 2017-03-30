#!/usr/bin/env python
"""
excuses.py - casca Excuse Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/casca/
"""

import re
from modules import proxy
import web


def excuse(casca, input):
    a = re.compile('<a [\s\S]+>(.*)</a>')

    try:
        page = proxy.get('http://programmingexcuses.com/')
    except:
        return casca.say("I'm all out of excuses!")

    results = a.findall(page)

    if results:
        result = results[0]
        result = result.strip()
        if result[-1] not in ['.', '?', '!']:
            result += '.'
        casca.say(result)
    else:
        casca.say("I'm too lazy to find an excuse.")
excuse.commands = ['excuse', 'excuses']


if __name__ == '__main__':
    print __doc__.strip()
