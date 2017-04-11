#!/usr/bin/env python
'''
strawpoll.py - casca Strawpoll Module
Copyright 2015, Bekey
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/
'''

import urllib2
import json
import shlex
import getopt

def create_strawpoll_json(title, arguments, multi, permissive):
    data = {'options':arguments,'title':title,'multi':multi,'permissive':permissive}
    return json.dumps(data)

def create_strawpoll_link(json_data):
    req = urllib2.Request('http://strawpoll.me/api/v2/polls')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Jenni)')

    response = urllib2.urlopen(req, json_data).read()
    strawpoll_id = json.loads(response)['id']
    return "http://strawpoll.me/" + str(strawpoll_id)

def strawpoll(casca, input):
    """ .strawpoll  --title='Example Title'
                    [--multi]
                    [--permissive]
                    'Option 1'
                    'Option 2'
                    'Option 3'

    Creates a strawpoll with the given title and options
    """

    if not input.admin:
        return;

    arguments = shlex.split(input)
    try:
        optlist, arguments = getopt.getopt(arguments[1:], 't:mp', ['title=', 'multi', 'permissive'])
    except getopt.GetoptError as err:
        return casca.say(str(err))

    multi = False
    permissive = False
    title = "N/A"

    for o, a in optlist:
        if o in ("-m", "--multi"):
            multi = True
        elif o in ("-p", "--permissive"):
            permissive = True
        elif o in ("-t", "--title"):
            title = a
        else:
            return casca.say("Unrecognized arguments.")

    if len(arguments) == 0:
        return casca.say("No options found.")

    if len(arguments) > 30:
        return casca.say("Cannot create strawpoll with more than 30 options.")

    try:
        data = create_strawpoll_json(title, arguments, multi, permissive)
        link = create_strawpoll_link(data)
    except Exception, e:
        return casca.say(str(e))

    if not hasattr(casca.config, "last_strawpoll"):
        casca.config.last_strawpoll = {}

    channel = input.sender
    casca.config.last_strawpoll[channel] = link

    casca.say(link)

strawpoll.commands = ['straw', 'strawpoll']
strawpoll.priority = 'medium'
strawpoll.example = '.strawpoll -t "Title Here" "Option 1" "Option 2" "Option 3"'

def resend_strawpoll(casca, input):
    """.resendstrawpoll - Resends the last strawpoll link created"""
    if hasattr(casca.config, "last_strawpoll"):
        channel = input.sender
        if channel in casca.config.last_strawpoll:
            return casca.say(casca.config.last_strawpoll[channel])
    casca.say("No Strawpoll links have been created yet.")

resend_strawpoll.commands = ['rsp', 'restraw', 'resendstrawpoll']
resend_strawpoll.priority = 'low'
resend_strawpoll.example = '.rsp'

if __name__ == "__main__":
    print __doc__.strip()
