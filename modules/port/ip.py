#!/usr/bin/env python
# coding=utf-8
"""
ip.py - casca IP Lookup Module
Copyright 2013, Michael Yanovich (yanovich.net)
Copyright 2011, Dimitri Molenaars (TyRope.nl)
Licensed under the Eiffel Forum License 2.

More info:
 * Willie: http://willie.dftba.net
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/

This module has been imported from Willie.
"""

from modules import unicode as uc
import json
import re
import socket
import web

base = 'http://freegeoip.net/json/'
re_ip = re.compile('(?i)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
re_country = re.compile('(?i)(.+), (.+ of)')

def ip_lookup(casca, input):
    txt = input.group(2)
    if not txt:
        return casca.reply("No search term!")
    txt = uc.encode(txt)
    query = uc.decode(txt)
    response = "[IP/Host Lookup] "
    try:
        page = web.get(base + txt)
    except IOError, err:
        return casca.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page)
    except:
        return casca.reply('Did not receive proper JSON from %s' % (base))
    if results:
        if re_ip.findall(query):
            ## IP Address
            try:
                hostname = socket.gethostbyaddr(query)[0]
            except:
                hostname = 'Unknown Host'
            response += 'Hostname: ' + str(hostname)
        else:
            ## Host name
            response += 'IP: ' + results['ip']
        spacing = ' |'
        for param in results:
            if not results[param]:
                results[param] = 'N/A'
        if 'city' in results:
            response += '%s City: %s' % (spacing, results['city'])
        if 'region_name' in results:
            response += '%s State: %s' % (spacing, results['region_name'])
        if 'country_name' in results:
            country = results['country_name']
            match = re_country.match(country)
            if match:
                country = ' '.join(reversed(match.groups()))
            response += '%s Country: %s' % (spacing, country)
        if 'zipcode' in results:
            response += '%s ZIP: %s' % (spacing, results['zipcode'])
        response += '%s Latitude: %s' % (spacing, results['latitude'])
        response += '%s Longitude: %s' % (spacing, results['longitude'])
    casca.reply(response)
ip_lookup.commands = ['ip', 'iplookup', 'host']
ip_lookup.example = ".iplookup 8.8.8.8"

if __name__ == '__main__':
    print __doc__.strip()
