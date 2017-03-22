#!/usr/bin/env python
"""
tell.py - casca Tell and Ask Module
Copyright 2012-2013, Michael Yanovich (yanovich.net)
Copyright 2008, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Phenny: http://inamidst.com/casca/
"""

import os, re, time, random
import threading

maximum = 4


def loadReminders(fn, lock):
    lock.acquire()
    try:
        result = {}
        f = open(fn)
        for line in f:
            line = line.strip()
            if line:
                try: tellee, teller, verb, timenow, msg = line.split('\t', 4)
                except ValueError: continue  # @@ hmm
                result.setdefault(tellee, []).append((teller, verb, timenow, msg))
        f.close()
    finally:
        lock.release()
    return result


def dumpReminders(fn, data, lock):
    lock.acquire()
    try:
        f = open(fn, 'w')
        for tellee in data.iterkeys():
            for remindon in data[tellee]:
                line = '\t'.join((tellee,) + remindon)
                try: f.write(line + '\n')
                except IOError: break
        try: f.close()
        except IOError: pass
    finally:
        lock.release()
    return True


def setup(self):
    fn = self.nick + '-' + self.config.host + '.tell.db'
    self.tell_filename = os.path.join(os.path.expanduser('~/.casca'), fn)
    if not os.path.exists(self.tell_filename):
        try: f = open(self.tell_filename, 'w')
        except OSError: pass
        else:
            f.write('')
            f.close()
    self.tell_lock = threading.Lock()
    self.reminders = loadReminders(self.tell_filename, self.tell_lock)  # @@ tell


def f_remind(casca, input):
    teller = input.nick

    #if hasattr(casca.config, 'logchan_pm'):
        #casca.msg(casca.config.logchan_pm, 'TELL used by %s in %s: %s' % (str(input.nick), str(input.sender), input))

    #if not input.group(2) or input.group(3):
    if not input.group(2):
        return casca.say('Please tell me who and what to tell people.')

    # @@ Multiple comma-separated tellees? Cf. Terje, #swhack, 2006-04-15
    line_prefix = (input.group()).lower()
    if input.group() and (line_prefix.startswith('.tell') or line_prefix.startswith('.yell')):
        verb = 'tell'.encode('utf-8')
        line = input.groups()
        line_txt = line[1].split()
        tellee = line_txt[0]
        msg = ' '.join(line_txt[1:])
        if line_prefix.startswith('.yell'):
            msg = (msg).upper()
    else:
        verb, tellee, msg = input.groups()

    ## handle unicode
    verb = verb.encode('utf-8')
    tellee = tellee.encode('utf-8')
    msg = msg.encode('utf-8')

    tellee = tellee.rstrip('.,:;')

    if not os.path.exists(casca.tell_filename):
        return

    timenow = time.strftime('%d %b %H:%MZ', time.gmtime())
    whogets = list()
    for tellee in tellee.split(','):
        if len(tellee) > 20:
            casca.say('Nickname %s is too long.' % (tellee))
            continue
        if not tellee.lower() in (teller.lower(), casca.nick):  # @@
            casca.tell_lock.acquire()
            try:
                if not tellee.lower() in whogets:
                    whogets.append(tellee)
                    if tellee not in casca.reminders:
                        casca.reminders[tellee] = [(teller, verb, timenow, msg)]
                    else:
                        casca.reminders[tellee].append((teller, verb, timenow, msg))
            finally:
                casca.tell_lock.release()
    response = str()
    if teller.lower() == tellee.lower() or tellee.lower() == 'me':
        response = 'You can %s yourself that.' % (verb)
    elif tellee.lower() == casca.nick.lower():
        response = "Hey, I'm not as stupid as Monty you know!"
    else:
        response = "I'll pass that on when %s is around."
        if len(whogets) > 1:
            listing = ', '.join(whogets[:-1]) + ', or ' + whogets[-1]
            response = response % (listing)
        elif len(whogets) == 1:
            response = response % (whogets[0])
        else:
            return casca.say('Huh?')

    if not whogets: # Only get cute if there are not legits
        rand = random.random()
        if rand > 0.9999: response = 'yeah, yeah'
        elif rand > 0.999: response = 'yeah, sure, whatever'

    casca.reply(response)

    dumpReminders(casca.tell_filename, casca.reminders, casca.tell_lock) # @@ tell
f_remind.rule = ('$nick', ['[tTyY]ell', '[aA]sk'], r'(\S+) (.*)')
f_remind.commands = ['tell', 'to', 'yell']


def getReminders(casca, channel, key, tellee):
    lines = []
    template = '%s: %s <%s> %s %s %s'
    today = time.strftime('%d %b', time.gmtime())

    casca.tell_lock.acquire()

    try:
        for (teller, verb, datetime, msg) in casca.reminders[key]:
            if datetime.startswith(today):
                datetime = datetime[len(today) + 1:]
            lines.append(template % (tellee, datetime, teller, verb, tellee, msg))

        try: del casca.reminders[key]
        except KeyError: casca.msg(channel, 'Er...')
    finally:
        casca.tell_lock.release()

    return lines


def message(casca, input):
    #if not input.sender.startswith('#'): return

    tellee = input.nick
    channel = input.sender

    if not os: return
    if not os.path.exists(casca.tell_filename):
        return

    reminders = []
    remkeys = list(reversed(sorted(casca.reminders.keys())))
    for remkey in remkeys:
        if not remkey.endswith('*') or remkey.endswith(':'):
            if tellee.lower() == remkey.lower():
                reminders.extend(getReminders(casca, channel, remkey, tellee))
        elif tellee.lower().startswith(remkey.rstrip('*:').lower()):
            reminders.extend(getReminders(casca, channel, remkey, tellee))

    for line in reminders[:maximum]:
        casca.say(line)

    if reminders[maximum:]:
        casca.say('Further messages sent privately')
        for line in reminders[maximum:]:
            casca.msg(tellee, line)

    if len(casca.reminders.keys()) != remkeys:
        dumpReminders(casca.tell_filename, casca.reminders, casca.tell_lock)  # @@ tell
message.rule = r'(.*)'
message.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
