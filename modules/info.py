#!/usr/bin/env python
"""
info.py - Casca Information Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://github.com/faxalter/casca/
"""


def help(casca, input):
    command = input.group(2)

    # work out a help URL to display
    if hasattr(casca.config, 'helpurl'):
        helpurl = casca.config.helpurl
    else:
        helpurl = "https://vtluug.org/wiki/Wadsworth"

    if input.sender.startswith('#'):
        # channels get a brief message instead
        casca.say(
            "Hey there, I'm a friendly bot for this channel. Say \".help\" "
            "to me in private for a list of my commands or check out my help "
            "page at {helpurl}.".format(
            helpurl=helpurl,
            owner=casca.config.owner))
    elif command is not None:
        command = command.lower()
        if command in casca.doc:
            casca.say(casca.doc[command][0])
            if casca.doc[command][1]: 
                casca.say('e.g. ' + casca.doc[command][1])
        else:
            casca.say("Sorry, I'm not that kind of bot.")
    else:
        commands = ', '.join(sorted(casca.doc.keys()))
        casca.say(
            "Hey there, I'm a friendly bot! Here are the commands I "
            "recognize: {commands}".format(commands=commands))
        casca.say(
            "For help with a command, just use .help followed by the name of"
            " the command, like \".help botsnack\".")
        casca.say(
            "If you need additional help can check out {helpurl} or you can "
            "talk to my owner, {owner}.".format(
            helpurl=helpurl,
            owner=casca.config.owner))
help.rule = (['help', 'command'], r'(.*)')
help.priority = 'low'


def stats(casca, input): 
    """Show information on command usage patterns."""
    commands = {}
    users = {}
    channels = {}

    ignore = set(['f_note', 'startup', 'message', 'noteuri', 'logger',
        'snarfuri', 'measure', 'messageAlert'])
    for (name, user), count in list(casca.stats.items()): 
        if name in ignore: continue
        if not user: continue

        if not user.startswith('#'): 
            try: users[user] += count
            except KeyError: users[user] = count
        else: 
            try: commands[name] += count
            except KeyError: commands[name] = count

            try: channels[user] += count
            except KeyError: channels[user] = count

    comrank = sorted([(b, a) for (a, b) in commands.items()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.items()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.items()], reverse=True)

    # most heavily used commands
    creply = 'most used commands: '
    for count, command in comrank[:10]: 
        creply += '%s (%s), ' % (command, count)
    casca.say(creply.rstrip(', '))

    # most heavy users
    reply = 'power users: '
    for count, user in userank[:10]: 
        reply += '%s (%s), ' % (user, count)
    casca.say(reply.rstrip(', '))

    # most heavy channels
    chreply = 'power channels: '
    for count, channel in charank[:3]: 
        chreply += '%s (%s), ' % (channel, count)
    casca.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'


if __name__ == '__main__':
    print(__doc__.strip())
