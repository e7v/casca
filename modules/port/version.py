#!/usr/bin/env python
"""
version.py - casca Version Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2009-2013, Silas Baronda
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/casca/
"""

from datetime import datetime
from subprocess import *


def git_info():
    p = Popen(['git', 'log', '-n 1'], stdout=PIPE, close_fds=True)

    commit = p.stdout.readline()
    author = p.stdout.readline()
    date = p.stdout.readline()
    return commit, author, date


def version(casca, input):
    commit, author, date = git_info()

    casca.say(str(input.nick) + ': running version:')
    casca.say('  ' + commit)
    casca.say('  ' + author)
    casca.say('  ' + date)
version.commands = ['version']
version.priority = 'medium'
version.rate = 10


def ctcp_version(casca, input):
    commit, author, date = git_info()
    date = date.replace('  ', '')

    casca.write(('NOTICE', input.nick),
            '\x01VERSION {0} : {1}\x01'.format(commit, date))
ctcp_version.rule = '\x01VERSION\x01'
ctcp_version.rate = 20


def ctcp_source(casca, input):
    casca.write(('NOTICE', input.nick),
            '\x01SOURCE https://github.com/myano/casca/\x01')
    casca.write(('NOTICE', input.nick),
            '\x01SOURCE\x01')
ctcp_source.rule = '\x01SOURCE\x01'
ctcp_source.rate = 10


def ctcp_ping(casca, input):
    text = input.group()
    text = text.replace('PING ', '')
    text = text.replace('\x01', '')
    casca.write(('NOTICE', input.nick),
            '\x01PING {0}\x01'.format(text))
ctcp_ping.rule = '\x01PING\s(.*)\x01'
ctcp_ping.rate = 10


def ctcp_time(casca, input):
    dt = datetime.now()
    current_time = dt.strftime('%A, %d. %B %Y %I:%M%p')
    casca.write(('NOTICE', input.nick),
            '\x01TIME {0}\x01'.format(current_time))
ctcp_time.rule = '\x01TIME\x01'
ctcp_time.rate = 10

if __name__ == '__main__':
    print __doc__.strip()
