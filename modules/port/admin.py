#!/usr/bin/env python
'''
admin.py - casca Admin Module
Copyright 2010-2013, Sean B. Palmer (inamidst.com) and Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
'''

import os
import time

intentional_part = False

def reload_confs(casca, input):
    # Reload known configs. This is an owner-only command.
    if not input.owner: return

    config_modules = []

    casca.config.config_helper.load_modules(config_modules)
    casca.reply("Reloaded configs")
reload_confs.commands = ['reload_configs', 'reload_config', 'reload_conf']
reload_confs.priority = 'low'

def join(casca, input):
    '''Join the specified channel. This is an owner-only command.'''
    # Can only be done in privmsg by an owner
    if input.sender.startswith('#'): return
    if not input.owner:
        return casca.say('You do not have owner privs.')
    incoming = input.group(2)
    if not incoming:
        return casca.say('Please provide some channels to join.')
    inc = incoming.split(' ')
    if len(inc) > 2:
        ## 3 or more inputs
        return casca.say('Too many inputs.')
    if input.owner:
        channel = inc[0]
        key = str()
        if len(inc) > 1:
            ## 2 inputs
            key = inc[1]
        if not key:
            casca.write(['JOIN'], channel)
        else: casca.write(['JOIN', channel, key])
join.commands = ['join']
join.priority = 'low'
join.example = '.join #example or .join #example key'

def part(casca, input):
    '''Part the specified channel. This is an admin-only command.'''
    # Can only be done in privmsg by an admin
    global intentional_part
    if input.sender.startswith('#'): return
    if input.admin:
        intentional_part = True
        casca.write(['PART'], input.group(2))
part.commands = ['part']
part.priority = 'low'
part.example = '.part #example'

def quit(casca, input):
    '''Quit from the server. This is an owner-only command.'''
    # Can only be done in privmsg by the owner
    if input.sender.startswith('#'): return
    if input.owner:
        casca.write(['QUIT'])
        __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'

def msg(casca, input):
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): return
    a, b = input.group(2), input.group(3)
    if (not a) or (not b): return
    if (a.startswith('+') or a.startswith('@')) and not input.owner:
        return
    al = a.lower()
    parts = al.split(',')
    if not input.owner:
        notallowed = ['chanserv', 'nickserv', 'hostserv', 'memoserv', 'saslserv', 'operserv']
        #if al == 'chanserv' or al == 'nickserv' or al == 'hostserv' or al == 'memoserv' or al == 'saslserv' or al == 'operserv':
        for each in notallowed:
            for part in parts:
                if part in notallowed:
                    return
    helper = False
    if hasattr(casca.config, 'helpers'):
        if a in casca.config.helpers and (input.host in casca.config.helpers[a] or (input.nick).lower() in casca.config.helpers[a]):
            helper = True
    if input.admin or helper:
        for part in parts:
            casca.msg(part, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.priority = 'low'

def me(casca, input):
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): return
    a, b = input.group(2), input.group(3)
    helper = False
    if hasattr(casca.config, 'helpers'):
        if a in casca.config.helpers and (input.host in casca.config.helpers[a] or (input.nick).lower() in casca.config.helpers[a]):
            helper = True
    if input.admin or helper:
        if a and b:
            msg = '\x01ACTION %s\x01' % input.group(3)
            casca.msg(input.group(2), msg, x=True)
me.rule = (['me'], r'(#?\S+) (.*)')
me.priority = 'low'


def defend_ground(casca, input):
    '''
    This function monitors all kicks across all channels casca is in. If she
    detects that she is the one kicked she'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if casca becomes
    annoying. Please use this with caution.
    '''
    channel = input.sender
    casca.write(['JOIN'], channel)
    time.sleep(10)
    casca.write(['JOIN'], channel)
defend_ground.event = 'KICK'
defend_ground.rule = '.*'
defend_ground.priority = 'low'


def defend_ground2(casca, input):
    global intentional_part
    if not intentional_part and input.nick == casca.config.nick:
        intentional_part = False
        channel = input.sender
        casca.write(['JOIN'], channel)
        time.sleep(10)
        casca.write(['JOIN'], channel)
defend_ground2.event = 'PART'
defend_ground2.rule = '.*'
defend_ground2.priority = 'low'


def blocks(casca, input):
    if not input.admin: return

    if hasattr(casca.config, 'logchan_pm') and input.sender != casca.config.logchan_pm:
        # BLOCKS USED - user in ##channel - text
        casca.msg(casca.config.logchan_pm, 'BLOCKS USED - %s in %s -- %s' % (input.nick, input.sender, input))

    STRINGS = {
            'success_del' : 'Successfully deleted block: %s',
            'success_add' : 'Successfully added block: %s',
            'no_nick' : 'No matching nick block found for: %s',
            'no_host' : 'No matching hostmask block found for: %s',
            'no_ident': 'No matching ident block found for: %s',
            'invalid' : 'Invalid format for %s a block. Try: .blocks add (nick|hostmask|ident) casca',
            'invalid_display' : 'Invalid input for displaying blocks.',
            'nonelisted' : 'No %s listed in the blocklist.',
            'huh' : 'I could not figure out what you wanted to do.',
            }

    if not os.path.isfile('blocks'):
        blocks = open('blocks', 'w')
        blocks.write('\n')
        blocks.close()

    blocks = open('blocks', 'r')
    contents = blocks.readlines()
    blocks.close()

    try: masks = contents[0].replace('\n', '').split(',')
    except: masks = ['']

    try: nicks = contents[1].replace('\n', '').split(',')
    except: nicks = ['']

    try: idents = contents[2].replace('\n', '').split(',')
    except: idents = ['']

    text = input.group().split()

    if len(text) == 3 and text[1] == 'list':
        ## Display all contents of the following

        ## Hostmasks
        if text[2] == 'hostmask':
            if len(masks) > 0 and masks.count('') == 0:
                for each in masks:
                    if len(each) > 0:
                        casca.say('blocked hostmask: ' + each)
            else:
                casca.reply(STRINGS['nonelisted'] % ('hostmasks'))

        ## Nicks
        elif text[2] == 'nick':
            if len(nicks) > 0 and nicks.count('') == 0:
                for each in nicks:
                    if len(each) > 0:
                        casca.say('blocked nick: ' + each)
            else:
                casca.reply(STRINGS['nonelisted'] % ('nicks'))

        elif text[2] == 'ident':
            if len(idents) > 0 and idents.count('') == 0:
                for each in idents:
                    if len(each) > 0:
                        casca.say('blocked ident: ' + each)

        ## Couldn't display anything
        else:
            casca.reply(STRINGS['invalid_display'])

    elif len(text) == 4 and text[1] == 'add':
        ## Add blocks...

        if text[2] == 'nick':
            nicks.append(text[3])
        elif text[2] == 'hostmask':
            masks.append(text[3])
        elif text[2] == 'ident':
            idents.append(text[3])
        else:
            casca.reply(STRINGS['invalid'] % ('adding'))
            return

        casca.reply(STRINGS['success_add'] % (text[3]))

    elif len(text) == 4 and text[1] == 'del':
        ## Delete a block...

        ## Nick
        if text[2] == 'nick':
            try:
                nicks.remove(text[3])
                casca.reply(STRINGS['success_del'] % (text[3]))
            except:
                casca.reply(STRINGS['no_nick'] % (text[3]))
                return

        ## Hostmask
        elif text[2] == 'hostmask':
            try:
                masks.remove(text[3])
                casca.reply(STRINGS['success_del'] % (text[3]))
            except:
                casca.reply(STRINGS['no_host'] % (text[3]))
                return

        ## Ident
        elif text[2] == 'ident':
            try:
                idents.remove(text[3])
                casca.reply(STRINGS['success_del'] % (text[3]))
            except:
                casca.reply(STRINGS['no_ident'] % (text[3]))
                return
        else:
            casca.reply(STRINGS['invalid'] % ('deleting'))
            return
    else:
        casca.reply(STRINGS['huh'])

    os.remove('blocks')
    blocks = open('blocks', 'w')

    masks_str = ','.join(masks)
    if len(masks_str) > 0 and ',' == masks_str[0]:
        masks_str = masks_str[1:]
    blocks.write(masks_str)

    blocks.write('\n')

    nicks_str = ','.join(nicks)
    if len(nicks_str) > 0 and ',' == nicks_str[0]:
        nicks_str = nicks_str[1:]
    blocks.write(nicks_str)

    blocks.write('\n')

    idents_str = ','.join(idents)
    if len(idents_str) > 0 and ',' == idents_str[0]:
        idents_str = idents_str[1:]
    blocks.write(idents_str)

    blocks.close()

blocks.commands = ['blocks']
blocks.priority = 'low'
blocks.thread = False

char_replace = {
        r'\x01': chr(1),
        r'\x02': chr(2),
        r'\x03': chr(3),
        }

def write_raw(casca, input):
    if not input.owner: return
    txt = input.bytes[7:]
    txt = txt.encode('utf-8')
    a = txt.split(':')
    status = False
    if len(a) > 1:
        newstr = u':'.join(a[1:])
        for x in char_replace:
            if x in newstr:
                newstr = newstr.replace(x, char_replace[x])
        casca.write(a[0].split(), newstr, raw=True)
        status = True
    elif a:
        b = a[0].split()
        casca.write([b[0].strip()], u' '.join(b[1:]), raw=True)
        status = True
    if status:
        casca.say('Message sent to server.')
write_raw.commands = ['write']
write_raw.priority = 'high'
write_raw.thread = False

if __name__ == '__main__':
    print __doc__.strip()

