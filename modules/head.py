#!/usr/bin/env python
"""
head.py - Phenny HTTP Metadata Utilities
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/casca/
"""

import re
import urllib.parse
import time
from html.entities import name2codepoint
import web
from tools import deprecated


def head(casca, input):
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '')
    if ' ' in uri:
        uri, header = uri.rsplit(' ', 1)
    else:
        uri, header = uri, None

    if not uri and hasattr(casca, 'last_seen_uri'):
        try:
            uri = casca.last_seen_uri[input.sender]
        except KeyError:
            return casca.say('?')

    if not uri.startswith('htt'):
        uri = 'http://' + uri
    # uri = uri.replace('#!', '?_escaped_fragment_=')
    start = time.time()

    try:
        info = web.head(uri)
        info['status'] = '200'
    except web.HTTPError as e:
        if hasattr(e, 'code'):
            return casca.say(str(e.code))
        else:
            return casca.say(str(e.response.status_code))
    except web.ConnectionError:
        return casca.say("Can't connect to %s" % uri)

    resptime = time.time() - start

    if header is None:
        data = []
        if 'Status' in info:
            data.append(info['Status'])
        if 'content-type' in info:
            data.append(info['content-type'].replace('; charset=', ', '))
        if 'last-modified' in info:
            modified = info['last-modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if 'content-length' in info:
            data.append(info['content-length'] + ' bytes')
        data.append('{0:1.2f} s'.format(resptime))
        casca.reply(', '.join(data))
    else:
        headerlower = header.lower()
        if headerlower in info:
            casca.say(header + ': ' + info.get(headerlower))
        else:
            msg = 'There was no %s header in the response.' % header
            casca.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'


r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')


def noteuri(casca, input):
    uri = input.group(1)
    if not hasattr(casca.bot, 'last_seen_uri'):
        casca.bot.last_seen_uri = {}
    casca.bot.last_seen_uri[input.sender] = uri
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'



def snarfuri(casca, input):
    uri = input.group(2)
    title = gettitle(casca, input, uri)

    if title:
        casca.msg(input.sender, title)
snarfuri.rule = r'([^\.].*)?(http[s]?://[^<> "\x01]+)[,.]?'
snarfuri.priority = 'low'
snarfuri.thread = True


def gettitle(casca, input, uri):
    if not ':' in uri:
        uri = 'http://' + uri
    uri = uri.replace('#!', '?_escaped_fragment_=')

    title = None
    localhost = [
        'http://localhost/', 'http://localhost:80/',
        'http://localhost:8080/', 'http://127.0.0.1/',
        'http://127.0.0.1:80/', 'http://127.0.0.1:8080/',
        'https://localhost/', 'https://localhost:80/',
        'https://localhost:8080/', 'https://127.0.0.1/',
        'https://127.0.0.1:80/', 'https://127.0.0.1:8080/',
    ]
    for s in localhost:
        if uri.startswith(s):
            return casca.reply('Sorry, access forbidden.')

    try:
        redirects = 0
        while True:
            info = web.head(uri)

            if not isinstance(info, list):
                status = '200'
            else:
                status = str(info[1])
                info = info[0]
            if status.startswith('3'):
                uri = urllib.parse.urljoin(uri, info['Location'])
            else:
                break

            redirects += 1
            if redirects >= 25:
                return None

        try:
            mtype = info['content-type']
        except:
            return None

        if not (('/html' in mtype) or ('/xhtml' in mtype)):
            return None

        bytes = web.get(uri)
        #bytes = u.read(262144)
        #u.close()

    except:
        return

    m = r_title.search(bytes)
    if m:
        title = m.group(1)
        title = title.strip()
        title = title.replace('\t', ' ')
        title = title.replace('\r', ' ')
        title = title.replace('\n', ' ')
        while '  ' in title:
            title = title.replace('  ', ' ')
        if len(title) > 200:
            title = title[:200] + '[...]'

        def e(m):
            entity = m.group(0)
            if entity.startswith('&#x'):
                cp = int(entity[3:-1], 16)
                return chr(cp)
            elif entity.startswith('&#'):
                cp = int(entity[2:-1])
                return chr(cp)
            else:
                char = name2codepoint[entity[1:-1]]
                return chr(char)
        title = r_entity.sub(e, title)

        if title:
            title = title.replace('\n', '')
            title = title.replace('\r', '')
            title = "[ {0} ]".format(title)

            if "posted" in casca.variables:
                from modules.posted import check_posted
                
                posted = check_posted(casca, input, uri)

                if posted:
                    title = "{0} (posted: {1})".format(title, posted)


        else:
            title = None
    return title


if __name__ == '__main__':
    print(__doc__.strip())
