#!/usr/bin/env python
"""
wikipedia.py - Casca Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://github.com/faxalter/casca/casca/
"""

import re
import web
import wiki

wikiapi = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json'
wikiuri = 'https://en.wikipedia.org/wiki/{0}'
wikisearch = 'https://en.wikipedia.org/wiki/Special:Search?' \
                          + 'search={0}&fulltext=Search'

def wik(casca, input): 
    """.wik <term> - Look up something on Wikipedia."""

    origterm = input.groups()[1]
    if not origterm: 
        return casca.say('Perhaps you meant ".wik Zen"?')

    term = web.unquote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    w = wiki.Wiki(wikiapi, wikiuri, wikisearch)

    try:
        result = w.search(term)
    except web.ConnectionError:
        error = "Can't connect to en.wikipedia.org ({0})".format(wikiuri.format(term))
        return casca.say(error)

    if result is not None: 
        casca.say(result)
    else:
        casca.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))

wik.commands = ['wik']
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
