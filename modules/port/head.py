#!/usr/bin/env python
"""
head.py - casca HTTP Metadata Utilities
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/
"""

import httplib, time
from htmlentitydefs import name2codepoint
from modules import proxy
import web


def head(casca, input):
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '').encode('utf-8')
    if ' ' in uri:
        uri, header = uri.rsplit(' ', 1)
    else: uri, header = uri, None

    if not uri and hasattr(casca, 'last_seen_uri'):
        try: uri = casca.last_seen_uri[input.sender]
        except KeyError: return casca.say('?')

    if not uri.startswith('htt'):
        uri = 'http://' + uri

    if '/#!' in uri:
        uri = uri.replace('/#!', '/?_escaped_fragment_=')

    try: info = proxy.head(uri)
    except IOError: return casca.say("Can't connect to %s" % uri)
    except httplib.InvalidURL: return casca.say("Not a valid URI, sorry.")

    if not isinstance(info, list):
        try: info = dict(info)
        except TypeError:
            return casca.reply('Try .head http://example.org/ [optional header]')
        info['Status'] = '200'
    else:
        newInfo = dict(info[0])
        newInfo['Status'] = str(info[1])
        info = newInfo

    if header is None:
        data = []
        if info.has_key('Status'):
            data.append(info['Status'])
        if info.has_key('content-type'):
            data.append(info['content-type'].replace('; charset=', ', '))
        if info.has_key('last-modified'):
            modified = info['last-modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if info.has_key('content-length'):
            data.append(info['content-length'] + ' bytes')
        casca.reply(', '.join(data))
    else:
        headerlower = header.lower()
        if info.has_key(headerlower):
            casca.say(header + ': ' + info.get(headerlower))
        else:
            msg = 'There was no %s header in the response.' % header
            casca.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'

if __name__ == '__main__':
    print __doc__.strip()
