#!/usr/bin/env python3
"""
sasl.py - casca SASL Authentication module
"""
import base64

def irc_cap (casca, input):
    cap, value = input.args[1], input.args[2]
    rq = ''

    if casca.is_connected:
        return

    if cap == 'LS':
        if 'multi-prefix' in value:
            rq += ' multi-prefix'
        if 'sasl' in value:
            rq += ' sasl'

        if not rq:
            irc_cap_end(casca, input)
        else:
            if rq[0] == ' ':
                rq = rq[1:]

            casca.write(('CAP', 'REQ', ':' + rq))

    elif cap == 'ACK':
        if 'sasl' in value:
            casca.write(('AUTHENTICATE', 'PLAIN'))
        else:
            irc_cap_end(casca, input)

    elif cap == 'NAK':
        irc_cap_end(casca, input)

    else:
        irc_cap_end(casca, input)

    return
irc_cap.rule = r'(.*)'
irc_cap.event = 'CAP'
irc_cap.priority = 'high'


def irc_authenticated (casca, input):
    auth = False
    if hasattr(casca.config, 'nick') and casca.config.nick is not None and hasattr(casca.config, 'password') and casca.config.password is not None:
        nick = casca.config.nick
        password = casca.config.password

        # If provided, use the specified user for authentication, otherwise just use the nick
        if hasattr(casca.config, 'user') and casca.config.user is not None:
            user = casca.config.user
        else:
            user = nick

        auth = "\0".join((nick, user, password))
        auth = base64.b64encode(auth)

    if not auth:
        casca.write(('AUTHENTICATE', '+'))
    else:
        while len(auth) >= 400:
            out = auth[0:400]
            auth = auth[401:]
            casca.write(('AUTHENTICATE', out))

        if auth:
            casca.write(('AUTHENTICATE', auth))
        else:
            casca.write(('AUTHENTICATE', '+'))

    return
irc_authenticated.rule = r'(.*)'
irc_authenticated.event = 'AUTHENTICATE'
irc_authenticated.priority = 'high'


def irc_903 (casca, input):
    casca.is_authenticated = True
    irc_cap_end(casca, input)
    return
irc_903.rule = r'(.*)'
irc_903.event = '903'
irc_903.priority = 'high'


def irc_904 (casca, input):
    irc_cap_end(casca, input)
    return
irc_904.rule = r'(.*)'
irc_904.event = '904'
irc_904.priority = 'high'


def irc_905 (casca, input):
    irc_cap_end(casca, input)
    return
irc_905.rule = r'(.*)'
irc_905.event = '905'
irc_905.priority = 'high'


def irc_906 (casca, input):
    irc_cap_end(casca, input)
    return
irc_906.rule = r'(.*)'
irc_906.event = '906'
irc_906.priority = 'high'


def irc_907 (casca, input):
    irc_cap_end(casca, input)
    return
irc_907.rule = r'(.*)'
irc_907.event = '907'
irc_907.priority = 'high'


def irc_001 (casca, input):
    casca.is_connected = True
    return
irc_001.rule = r'(.*)'
irc_001.event = '001'
irc_001.priority = 'high'


def irc_cap_end (casca, input):
    casca.write(('CAP', 'END'))
    return


if __name__ == '__main__':
    print(__doc__.strip())
