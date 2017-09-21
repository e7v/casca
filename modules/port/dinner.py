#!/usr/bin/env python
'''
dinner.py - Dinner Module
Copyright 2014 Sujeet Akula (sujeet@freeboson.org)
Copyright 2013 Michael Yanovich (yanovich.net)
Copyright 2013 Unknown
Licensed under the Eiffel Forum License 2.

More info:
 * casca-misc: https://github.com/freeboson/casca-misc/
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
'''

import re
import web
from modules.url import short

re_mark = re.compile('<dt><a href="(.*?)" target="_blank">(.*?)</a></dt>')

def fucking_dinner(casca, input):
    '''.fd -- provide suggestions for dinner'''
    txt = input.group(2)
    url = 'http://www.whatthefuckshouldimakefordinner.com'
    if txt == '-v':
        url = 'http://whatthefuckshouldimakefordinner.com/veg.php'
    page = web.get(url)

    results = re_mark.findall(page)

    if results:

        dish = results[0][1].upper()
        long_url = results[0][0]

        try:
            short_url = short(long_url)[0][1]
        except:
            short_url = long_url

        casca.say("WHY DON'T YOU EAT SOME FUCKING: " + dish +
                  " HERE IS THE RECIPE: " + short_url)

    else:
        casca.say("I DON'T FUCKING KNOW, EAT PIZZA.")

fucking_dinner.commands = ['fucking_dinner', 'fd', 'wtfsimfd']
fucking_dinner.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
