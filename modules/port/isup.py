#!/usr/bin/env python
"""
isup.py - Simple website status check with isup.me
Copyright 2013-2014, Michael Yanovich (yanovich.net)
Copyright 2012-2013 Edward Powell (embolalaia.net)
Licensed under the Eiffel Forum License 2.

This allows users to check if a website is up through isup.me.

More info:
 * Willie: http://willie.dftba.net/
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

from modules import proxy
import re
import web


def isup(casca, input):
    '''isup.me website status checker'''
    site = input.group(2)
    if not site:
        return casca.reply('What site do you want to check?')
    if ' ' in site:
        idx = site.find(' ')
        site = site[:idx+1]
    site = (site).strip()

    if site[:7] != 'http://' and site[:8] != 'https://':
        if '://' in site:
            protocol = site.split('://')[0] + '://'
            return casca.reply('Try it again without the %s' % protocol)
        else:
            site = 'http://' + site
    try:
        response = proxy.get(site)
    except Exception as e:
        casca.say(site + ' looks down from here.')
        return

    if response:
        casca.say(site + ' looks fine to me.')
    else:
        casca.say(site + ' is down from here.')
isup.commands = ['isup']
isup.example = '.isup google.com'

if __name__ == '__main__':
    print __doc__.strip()
