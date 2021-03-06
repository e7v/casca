#!/usr/bin/env python
"""
why.py - casca Why Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

import re
import web

whyuri = 'http://www.leonatkinson.com/random/index.php/rest.html?method=advice'
r_paragraph = re.compile(r'<quote>.*?</quote>')


def getwhy(casca, input):
    page = web.get(whyuri)
    paragraphs = r_paragraph.findall(page)
    out = str()
    if paragraphs:
        line = re.sub(r'<[^>]*?>', '', unicode(paragraphs[0]))
        out = line.lower().capitalize() + "."
    else:
        out = 'We are unable to find any reasons *why* this should work.'

    return casca.say(out)
getwhy.commands = ['why', 'tubbs']
getwhy.thread = False
getwhy.rate = 30

if __name__ == '__main__':
    print __doc__.strip()
